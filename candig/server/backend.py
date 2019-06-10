"""
Module responsible for handling protocol requests and returning
responses.
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import candig.server.datamodel as datamodel
import candig.server.exceptions as exceptions
import candig.server.paging as paging
import candig.server.response_builder as response_builder
import candig.schemas.protocol as protocol
import operator
from google.protobuf.json_format import MessageToDict
import json
import itertools
import DP as DP


class Backend(object):
    """
    Backend for handling the server requests.
    This class provides methods for all of the GA4GH protocol end points.
    """
    def __init__(self, dataRepository):
        self._requestValidation = False
        self._defaultPageSize = 1800
        self._maxResponseLength = 2**20  # 1 MiB
        self._dataRepository = dataRepository
        self._dpEpsilon = None

        self.ops = {
            ">": operator.gt,
            "gt": operator.gt,
            "<": operator.lt,
            "lt": operator.lt,
            ">=": operator.ge,
            "ge": operator.ge,
            "<=": operator.le,
            "le": operator.le,
            "eq": operator.eq,
            "=": operator.eq,
            "==": operator.eq,
            "!=": operator.ne,
            "ne": operator.ne,
            "contains": operator.contains
        }

        self.endpointMapper = {
            "patients": self.runSearchPatients,
            "enrollments": self.runSearchEnrollments,
            "consents": self.runSearchConsents,
            "diagnoses": self.runSearchDiagnoses,
            "samples": self.runSearchSamples,
            "treatments": self.runSearchTreatments,
            "outcomes": self.runSearchOutcomes,
            "complications": self.runSearchComplications,
            "tumourboards": self.runSearchTumourboards,
            "variantsByGene": self.runSearchVariantsByGeneName,
            "variants": self.runSearchVariants,
            "slides": self.runSearchSlides,
            "studies": self.runSearchStudies,
            "labtests": self.runSearchLabtests,
            "surgeries": self.runSearchSurgeries,
            "chemotherapies": self.runSearchChemotherapies,
            "immunotherapies": self.runSearchImmunotherapies,
            "radiotherapies": self.runSearchRadiotherapies,
            "celltransplants": self.runSearchCelltransplants
        }

    def getDataRepository(self):
        """
        Get the data repository used by this backend
        """
        return self._dataRepository

    def setRequestValidation(self, requestValidation):
        """
        Set enabling request validation
        """
        self._requestValidation = requestValidation

    def setDefaultPageSize(self, defaultPageSize):
        """
        Sets the default page size for request to the specified value.
        """
        self._defaultPageSize = defaultPageSize

    def setMaxResponseLength(self, maxResponseLength):
        """
        Sets the approximate maximum response length to the specified
        value.
        """
        self._maxResponseLength = maxResponseLength

    def setDpEpsilon(self, epsilon):
        """
        Sets the epsilon value used in differential privacy functions
        """
        self._dpEpsilon = epsilon

    def startProfile(self):
        """
        Profiling hook. Called at the start of the runSearchRequest method
        and allows for detailed profiling of search performance.
        """
        pass

    def endProfile(self):
        """
        Profiling hook. Called at the end of the runSearchRequest method.
        """
        pass

    # Iterators over the data hierarchy. These methods help to
    # implement the search endpoints by providing iterators
    # over the objects to be returned to the client.

    def _topLevelObjectGenerator(self, request, numObjects, getByIndexMethod, tier=0):
        """
        Returns a generator over the results for the specified request, which
        is over a set of objects of the specified size. The objects are
        returned by call to the specified method, which must take a single
        integer as an argument. The returned generator yields a sequence of
        (object, nextPageToken) pairs, which allows this iteration to be picked
        up at any point.
        """
        currentIndex = 0
        if request.page_token:
            currentIndex, = paging._parsePageToken(
                request.page_token, 1)
        while currentIndex < numObjects:
            object_ = getByIndexMethod(currentIndex)
            currentIndex += 1
            nextPageToken = None
            if currentIndex < numObjects:
                nextPageToken = str(currentIndex)
            yield object_.toProtocolElement(tier), nextPageToken

    def _protocolObjectGenerator(self, request, numObjects, getByIndexMethod):
        """
        Returns a generator over the results for the specified request, from
        a set of protocol objects of the specified size. The objects are
        returned by call to the specified method, which must take a single
        integer as an argument. The returned generator yields a sequence of
        (object, nextPageToken) pairs, which allows this iteration to be picked
        up at any point.
        """
        currentIndex = 0
        if request.page_token:
            currentIndex, = paging._parsePageToken(
                request.page_token, 1)
        while currentIndex < numObjects:
            object_ = getByIndexMethod(currentIndex)
            currentIndex += 1
            nextPageToken = None
            if currentIndex < numObjects:
                nextPageToken = str(currentIndex)
            yield object_, nextPageToken

    def _protocolListGenerator(self, request, objectList):
        """
        Returns a generator over the objects in the specified list using
        _protocolObjectGenerator to generate page tokens.
        """
        return self._protocolObjectGenerator(
            request, len(objectList), lambda index: objectList[index])

    def _objectListGenerator(self, request, objectList, tier=0):
        """
        Returns a generator over the objects in the specified list using
        _topLevelObjectGenerator to generate page tokens.
        """
        return self._topLevelObjectGenerator(
            request,
            len(objectList),
            lambda index: objectList[index],
            tier=tier,
        )

    def datasetsGenerator(self, request, access_map):
        """
        Returns a generator over the (dataset, nextPageToken) pairs
        defined by the specified request
        """
        return self._topLevelAuthzDatasetGenerator(
            request, self.getDataRepository().getNumDatasets(),
            self.getDataRepository().getAuthzDatasetByIndex, access_map=access_map)

    # SEARCH
    def queryGenerator(self, request, return_mimetype, access_map, count=False):
        """
        Generator object for advanced search queries
        """
        parsedRequest = MessageToDict(request)

        try:
            dataset_id = parsedRequest["datasetId"]
            logic = parsedRequest["logic"]
            components = parsedRequest["components"]
            results = parsedRequest["results"]
        except KeyError as error:
            raise exceptions.MissingFieldNameException(error.message)

        responses = self.componentsHandler(dataset_id, components, return_mimetype, access_map)
        patient_list = self.logicHandler(logic, responses, dataset_id, access_map)
        page_token = parsedRequest.get("pageToken")

        return self.resultsHandler(results, patient_list, dataset_id, return_mimetype, access_map, page_token, count)

    def logicHandler(self, logic, responses, dataset_id, access_map):
        """
        :param  logic: dict parsed from query containing logic statement keys or component id keys
        :param  responses: object with key being the id, and the value being the response from corresponding endpoints
        :param  dataset_id: unique dataset id
        :param  access_map: user access levels for authz
        :return: list of patient_id filtered based on join logic
        """

        op_keys = ['and', 'or']
        logic_negate = False

        if len(logic.keys()) == 1:
            logic_key = logic.keys()[0]
        elif len(logic.keys()) == 2:
            if {'id', 'negate'} == set(logic.keys()):
                logic_key = 'id'
                logic_negate = bool(logic['negate'])
            else:
                raise exceptions.InvalidLogicException("Invalid key combination")
        else:
            raise exceptions.InvalidLogicException('Invalid number of keys')

        if logic_key in op_keys:
            results_arr = []
            patient_set = set()

            for logic_obj in logic[logic_key]:
                results_arr.append(set(self.logicHandler(logic_obj, responses, dataset_id, access_map)))

            if logic_key == 'or':
                for id_set in results_arr:
                    for patient_id in id_set:
                        patient_set.add(patient_id)
            elif logic_key == 'and':
                results_arr.sort(key=len)
                for patient_id in results_arr[0]:
                    if all(patient_id in results_arr[x] for x in range(1, len(results_arr))):
                        patient_set.add(patient_id)
            return list(patient_set)

        elif logic_key == 'id':
            id_set = set()

            try:
                for response in responses[logic[logic_key]]:
                    patient_id = self.getResponsePatientId(response, dataset_id)
                    id_set.add(patient_id)
                if logic_negate:
                    id_list_all = self.getAllPatientId(dataset_id, access_map)
                    id_set = set(id_list_all) - id_set
                
                id_list = list(id_set)
                return id_list

            except KeyError:
                raise exceptions.InvalidLogicException("Given id does not match a component")

        else:
            # invalid logic key
            raise exceptions.InvalidLogicException("Invalid key used")

    def getAllPatientId(self, dataset_id, access_map):
        """
        Return all available patient id for the dataset on the local server
        :param  dataset_id: unique dataset id
        :param  access_map: user access levels for authz
        :return: patient id list
        """
        request = json.dumps({"dataset_id": dataset_id})
        all_pt = json.loads(self.runSearchPatients(request, 'application/json', access_map))
        return [pt["patientId"] for pt in all_pt["patients"]]

    def getResponsePatientId(self, response, dataset_id):
        """
        Gets the patientId from the response for object joins, otherwise throw error
        :param response:
        :param dataset_id:
        :return: patient id string
        """
        if 'patientId' in response:
            return response['patientId']
        elif 'variantSetId' in response:
            dataset = self.getDataRepository().getDataset(dataset_id)
            variantSet = dataset.getVariantSet(response['variantSetId'])
            return variantSet.getPatientId()
        else:
            raise exceptions.BadRequestException

    def componentsHandler(self, datasetId, components, return_mimetype, access_map):
        """
        Parse the component portion of incoming request
        :param datasetId;
        :param components:
        :param access_map
        :return: responses object with key being the id, and the value being the response from corresponding endpoints
        """
        requests = {}
        idMapper = {}

        for component in components:
            keyList = list(component.keys())
            if len(keyList) != 2:
                raise exceptions.MissingFieldNameException("Missing or invalid component fields")
            keyList.remove('id')
            endpoint = keyList[0]

            request = {"datasetId": datasetId}

            try:
                if endpoint == "variants":
                    request["start"] = component[endpoint]["start"]
                    request["end"] = component[endpoint]["end"]
                    request["referenceName"] = component[endpoint]["referenceName"]
                    if "variantSetIds" in component[endpoint]:
                        request["variantSetIds"] = component[endpoint]["variantSetIds"]
                        # variants/search will throw 400 is both datasetId and variantSetIds are specified
                        request.pop('datasetId', None)

                elif endpoint == "variantsByGene":
                    request["gene"] = component[endpoint]["gene"]

                else:
                    if "filters" in component[endpoint]:
                        request["filters"] = component[endpoint]["filters"]

            except KeyError as error:
                raise exceptions.MissingFieldNameException(str(error))

            idMapper[component["id"]] = endpoint
            requests[component["id"]] = request

        return self.endpointCaller(requests, idMapper, return_mimetype, access_map)

    def endpointCaller(self, requests, idMapper, return_mimetype, access_map):
        """
        Call all endpoints returned by componentsHandler
        :param requests:
        :return responses object with key being the id, and the value being the response from corresponding endpoints
        """
        responses = {}

        for key in requests:
            requestStr = json.dumps(requests[key])

            responseObj = json.loads(
                self.endpointMapper[idMapper[key]](requestStr, return_mimetype, access_map)
            )

            try:
                # TODO: this work around could probably be improved
                if idMapper[key] == "variantsByGene":
                    idMapper[key] = "variants"
                responses[key] = responseObj[idMapper[key]]
            except KeyError:
                responses[key] = []

            nextToken = responseObj.get('nextPageToken')

            while nextToken:
                request = json.loads(requestStr)
                request["page_token"] = nextToken
                requestStr = json.dumps(request)

                nextPageRequest = json.loads(
                    self.endpointMapper[idMapper[key]](requestStr, return_mimetype, access_map)
                )

                responses[key] += nextPageRequest[idMapper[key]]
                nextToken = nextPageRequest.get('nextPageToken')

        return responses

    def resultsHandler(self, results, patient_list, dataset_id, return_mimetype, access_map, page_token, count):
        """
        :param results:
        :return:
        """

        # generatorMapper = {
        #     "patients": self.patientsGenerator,
        #     "enrollments": self.enrollmentsGenerator,
        #     "consents": self.consentsGenerator,
        #     "diagnoses": self.diagnosesGenerator,
        #     "samples": self.samplesGenerator,
        #     "treatments": self.treatmentsGenerator,
        #     "outcomes": self.outcomesGenerator,
        #     "complications": self.complicationsGenerator,
        #     "tumourboards": self.tumourboardsGenerator
        # }

        # protocolMapper = {
        #     "patients": protocol.SearchPatientsRequest,
        #     "enrollments": protocol.SearchEnrollmentsRequest,
        #     "consents": protocol.SearchConsentsRequest,
        #     "diagnoses": protocol.SearchDiagnosesRequest,
        #     "samples": protocol.SearchSamplesRequest,
        #     "treatments": protocol.SearchTreatmentsRequest,
        #     "outcomes": protocol.SearchOutcomesRequest,
        #     "complications": protocol.SearchComplicationsRequest,
        #     "tumourboards": protocol.SearchTumourboardsRequest
        # }

        table = results[0].get("table")
        field = results[0].get("fields")

        if count and not field:
            raise exceptions.MissingFieldNameException("Fields list required for count query")

        if table is None:
            raise exceptions.MissingFieldNameException("table")
        elif table not in self.endpointMapper:
            raise exceptions.MissingFieldNameException("Invalid results table specified")

        # If patient list is empty, return an empty response
        if len(patient_list) == 0:
            if table == "variantsByGene":
                table = "variants"

            results = {}
            results[table] = []
            return json.dumps(results)

        # TODO: Handle returning other table types e.g. variants
        if table == "variantsByGene" or table == "variants":
            results = self.variantsResultsHandler(table, results, patient_list, dataset_id,
                                                  return_mimetype, access_map, page_token)

        else:
            request = {
                "datasetId": dataset_id,
                "filters": [{
                    "field": "patientId",
                    "operator": "in",
                    "values": patient_list
                }]
            }

            if page_token:
                request["page_token"] = page_token

            requestStr = json.dumps(request)

            results = self.endpointMapper[table](requestStr, return_mimetype, access_map)

        # perform count based on field aggregation (/count endpoint)
        if count:
            results = self.aggregationHandler(table, results, field)

        # filter results on given field list (/search endpoint)
        elif field:
            results = self.fieldHandler(table, results, field)

        # returns empty list instead of 404
        if not json.loads(results):
            results = json.dumps({table: []})

        return results

    def fieldHandler(self, table, results, field):
        """
        Modifies results object to return only specified fields
        :param table: db table from which results are being returned
        :param results: query results
        :param field: array of field names to return
        :return: formatted results in string representation
        """
        json_results = json.loads(results)
        json_array = json_results.get(table, [])
        filtered_results = []
        for entry in json_array:
            field_obj = {k: entry[k] for k in field if k in entry}
            if field_obj:
                filtered_results.append(field_obj)
        response_obj = {}
        if filtered_results:
            response_obj = {table: filtered_results}
        return json.dumps(response_obj)

    def aggregationHandler(self, table, results, field):
        """
        Aggregates results based on specified fields and returns counts for each value
        :param table: db table from which results are being returned
        :param results: query results
        :param field: array of field names to aggregate on
        :return: formatted results in string representation
        """
        json_results = json.loads(results)
        field_value_counts = {}
        if table == "variantsByGene":
            table = "variants"
        try:
            for entry in json_results[table]:
                for k, v in entry.iteritems():
                    if k in field:
                        if k not in field_value_counts:
                            field_value_counts[k] = {}

                        if type(v) == list:
                            v.sort()
                            v = ','.join(v)

                        if v not in field_value_counts[k]:
                            field_value_counts[k][v] = 1
                        else:
                            field_value_counts[k][v] += 1
        except KeyError:
            field_value_counts = {}

        agg_results = self.countHelper(table, field_value_counts)
        if "nextPageToken" in json_results:
            agg_results["nextPageToken"] = json_results["nextPageToken"]
        return json.dumps(agg_results)

    def countHelper(self, table, fv_counts):
        """
        Formats count results and applies differential privacy if set in backend
        :param table: db table from which results are being returned
        :param fv_counts: dict containing value based counts for each field
        :return: formatted results object
        """
        response_list = []
        if fv_counts:
            if self._dpEpsilon:
                ndp = DP.DP(fv_counts, eps=self._dpEpsilon)
                ndp.get_noise()
            response_list.append(fv_counts)
        return {table: response_list}

    def variantsResultsHandler(self, table, results, patient_list, dataset_id, return_mimetype, access_map, page_token):

        request = {}

        if table == "variantsByGene":
            gene = results[0].get("gene")

            if gene is None:
                raise exceptions.MissingGeneNameException

            else:
                request = {
                    "datasetId": dataset_id,
                    "patientList": patient_list,
                    "gene": gene
                }

        elif table == "variants":
            start = results[0].get("start")
            end = results[0].get("end")
            referenceName = results[0].get("referenceName")

            if start is None or end is None or referenceName is None:
                raise exceptions.MissingVariantKeysException

            else:
                request = {
                    "datasetId": dataset_id,
                    "patientList": patient_list,
                    "start": start,
                    "end": end,
                    "referenceName": referenceName
                }

        if page_token:
            request["page_token"] = page_token

        requestStr = json.dumps(request)

        return self.runSearchVariantsByGeneName(requestStr, return_mimetype, access_map)

    def experimentsGenerator(self, request, tier=0):
        """
        Returns a generator over the (experiment, nextPageToken) pairs
        defined by the specified request
        TODO: This should really be under the appropriate biosamples, but
        for now..
        """
        return self._topLevelObjectGenerator(
            request, self.getDataRepository().getNumExperiments(),
            self.getDataRepository().getExperimentByIndex)

    def analysesGenerator(self, request, tier=0):
        """
        Returns a generator over the (analysis, nextPageToken) pairs
        defined by the specified request
        TODO: This should really be under the appropriate biosamples, but
        for now..
        """
        return self._topLevelObjectGenerator(
            request, self.getDataRepository().getNumAnalyses(),
            self.getDataRepository().getAnalysisByIndex)

    def biosamplesGenerator(self, request, tier=0):
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        results = []
        for obj in dataset.getBiosamples():
            include = True
            if request.name:
                if request.name != obj.getLocalId():
                    include = False
            if request.individual_id:
                if request.individual_id != obj.getIndividualId():
                    include = False
            if include:
                results.append(obj)
        return self._objectListGenerator(request, results)

    def individualsGenerator(self, request, tier=0):
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        results = []
        for obj in dataset.getIndividuals():
            include = True
            if request.name:
                if request.name != obj.getLocalId():
                    include = False
            if include:
                results.append(obj)
        return self._objectListGenerator(request, results)

    def comparisonGenerator(self, obj, filters):
        """
        Apply the specified operator to determine if an object is valid for the request
        :param obj: The candidate object
        :param filters: The filters
        :return: True if the object is qualified, False otherwise.
        """
        qualified = True

        try:
            for filter in filters:
                if "value" not in filter:
                    if "values" not in filter:
                        qualified = False
                        break
                    else:
                        if obj.mapper(filter["field"]) not in filter["values"]:
                            qualified = False
                            break
                elif not self.ops[filter["operator"].lower()](obj.mapper(filter["field"]), filter["value"]):
                        qualified = False
                        break
        except TypeError:
            raise exceptions.BadInputTypeException
        except (KeyError, AttributeError):
            raise exceptions.BadFilterKeyException

        return qualified

    def filtersValidator(self, request):

        filters = MessageToDict(request).get("filters", [])

        for filt in filters:

            if "field" not in filt or "operator" not in filt:
                raise exceptions.BadRequestException("Please specify field and/or operator in your filters.")

            elif "value" in filt and "values" in filt:
                raise exceptions.BadRequestException("You can only specify one of value or values in one filter.")

            elif "value" in filt:
                if filt["operator"] == "in":
                    raise exceptions.BadRequestException("You can only use the in operator when you supply a list of values in your filter, specify 'values' instead of 'value'.")

            elif "values" in filt:
                if filt["operator"] != "in":
                    raise exceptions.BadRequestException("If you specify a list of values in your filter, the operator has to be in.")

                filt["values"] = set(filt["values"])

            else:
                raise exceptions.BadRequestException("You need to specify one of value or values in one filter.")

        return filters

    def patientsGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getPatients():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)

        return self._objectListGenerator(request, results, tier=tier)

    def enrollmentsGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getEnrollments():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)

        return self._objectListGenerator(request, results, tier=tier)

    def consentsGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getConsents():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)

        return self._objectListGenerator(request, results, tier=tier)

    def diagnosesGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getDiagnoses():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)

        return self._objectListGenerator(request, results, tier=tier)

    def samplesGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getSamples():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)
        return self._objectListGenerator(request, results, tier=tier)

    def treatmentsGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getTreatments():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)
        return self._objectListGenerator(request, results, tier=tier)

    def outcomesGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getOutcomes():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)
        return self._objectListGenerator(request, results, tier=tier)

    def complicationsGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getComplications():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)
        return self._objectListGenerator(request, results, tier=tier)

    def tumourboardsGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getTumourboards():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)
        return self._objectListGenerator(request, results, tier=tier)

    def chemotherapiesGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getChemotherapies():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)
        return self._objectListGenerator(request, results, tier=tier)

    def radiotherapiesGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getRadiotherapies():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)
        return self._objectListGenerator(request, results, tier=tier)

    def surgeriesGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getSurgeries():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)
        return self._objectListGenerator(request, results, tier=tier)

    def immunotherapiesGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getImmunotherapies():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)
        return self._objectListGenerator(request, results, tier=tier)

    def celltransplantsGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getCelltransplants():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)
        return self._objectListGenerator(request, results, tier=tier)

    def slidesGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getSlides():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)
        return self._objectListGenerator(request, results, tier=tier)

    def studiesGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getStudies():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)
        return self._objectListGenerator(request, results, tier=tier)

    def labtestsGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getLabtests():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)
        return self._objectListGenerator(request, results, tier=tier)

    def extractionsGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getExtractions():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)
        return self._objectListGenerator(request, results, tier=tier)

    def sequencingGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getSequencings():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)
        return self._objectListGenerator(request, results, tier=tier)

    def alignmentsGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getAlignments():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)
        return self._objectListGenerator(request, results, tier=tier)

    def variantCallingGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getVariantCallings():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)
        return self._objectListGenerator(request, results, tier=tier)

    def fusionDetectionGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getFusionDetections():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)
        return self._objectListGenerator(request, results, tier=tier)

    def expressionAnalysisGenerator(self, request, access_map):
        """
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        results = []
        filters = self.filtersValidator(request)

        for obj in dataset.getExpressionAnalyses():
            qualified = self.comparisonGenerator(obj, filters)

            if qualified:
                results.append(obj)
        return self._objectListGenerator(request, results, tier=tier)

    def phenotypeAssociationSetsGenerator(self, request, access_map):
        """
        Returns a generator over the (phenotypeAssociationSet, nextPageToken)
        pairs defined by the specified request
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        return self._topLevelObjectGenerator(
            request, dataset.getNumPhenotypeAssociationSets(),
            dataset.getPhenotypeAssociationSetByIndex)

    def readGroupSetsGenerator(self, request, access_map):
        """
        Returns a generator over the (readGroupSet, nextPageToken) pairs
        defined by the specified request.
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        return self._readGroupSetsGenerator(
            request, dataset.getNumReadGroupSets(),
            dataset.getReadGroupSetByIndex)

    def _readGroupSetsGenerator(self, request, numObjects, getByIndexMethod):
        """
        Returns a generator over the results for the specified request, which
        is over a set of objects of the specified size. The objects are
        returned by call to the specified method, which must take a single
        integer as an argument. The returned generator yields a sequence of
        (object, nextPageToken) pairs, which allows this iteration to be picked
        up at any point.
        """
        currentIndex = 0
        if request.page_token:
            currentIndex, = paging._parsePageToken(
                request.page_token, 1)
        while currentIndex < numObjects:
            obj = getByIndexMethod(currentIndex)
            include = True
            rgsp = obj.toProtocolElement()
            if request.name and request.name != obj.getLocalId():
                include = False
            if request.biosample_id and include:
                rgsp.ClearField(b"read_groups")
                for readGroup in obj.getReadGroups():
                    if request.biosample_id == readGroup.getBiosampleId():
                        rgsp.read_groups.extend(
                            [readGroup.toProtocolElement()])
                # If none of the biosamples match and the readgroupset
                # contains reagroups, don't include in the response
                if len(rgsp.read_groups) == 0 and \
                        len(obj.getReadGroups()) != 0:
                    include = False
            currentIndex += 1
            nextPageToken = None
            if currentIndex < numObjects:
                nextPageToken = str(currentIndex)
            if include:
                yield rgsp, nextPageToken

    def referenceSetsGenerator(self, request, access_map):
        """
        Returns a generator over the (referenceSet, nextPageToken) pairs
        defined by the specified request.
        """
        results = []
        for obj in self.getDataRepository().getReferenceSets():
            include = True
            if request.md5checksum:
                if request.md5checksum != obj.getMd5Checksum():
                    include = False
            if request.accession:
                if request.accession not in obj.getSourceAccessions():
                    include = False
            if request.assembly_id:
                if request.assembly_id != obj.getAssemblyId():
                    include = False
            if include:
                results.append(obj)
        return self._objectListGenerator(request, results)

    def referencesGenerator(self, request, access_map):
        """
        Returns a generator over the (reference, nextPageToken) pairs
        defined by the specified request.
        """
        referenceSet = self.getDataRepository().getReferenceSet(
            request.reference_set_id)
        results = []
        for obj in referenceSet.getReferences():
            include = True
            if request.md5checksum:
                if request.md5checksum != obj.getMd5Checksum():
                    include = False
            if request.accession:
                if request.accession not in obj.getSourceAccessions():
                    include = False
            if include:
                results.append(obj)
        return self._objectListGenerator(request, results)

    def variantSetsGenerator(self, request, access_map):
        """
        Returns a generator over the (variantSet, nextPageToken) pairs defined
        by the specified request.
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        self.getUserAccessTier(dataset, access_map)
        return self._topLevelObjectGenerator(
            request, dataset.getNumVariantSets(),
            dataset.getVariantSetByIndex)

    def variantAnnotationSetsGenerator(self, request, access_map):
        """
        Returns a generator over the (variantAnnotationSet, nextPageToken)
        pairs defined by the specified request.
        """
        compoundId = datamodel.VariantSetCompoundId.parse(
            request.variant_set_id)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        self.getUserAccessTier(dataset, access_map)
        variantSet = dataset.getVariantSet(request.variant_set_id)
        return self._topLevelObjectGenerator(
            request, variantSet.getNumVariantAnnotationSets(),
            variantSet.getVariantAnnotationSetByIndex)

    def readsGenerator(self, request, access_map):
        """
        Returns a generator over the (read, nextPageToken) pairs defined
        by the specified request
        """
        if not request.reference_id:
            raise exceptions.UnmappedReadsNotSupported()
        if len(request.read_group_ids) < 1:
            raise exceptions.BadRequestException(
                "At least one readGroupId must be specified")
        elif len(request.read_group_ids) == 1:
            return self._readsGeneratorSingle(request, access_map)
        else:
            return self._readsGeneratorMultiple(request, access_map)

    def _readsGeneratorSingle(self, request, access_map):
        compoundId = datamodel.ReadGroupCompoundId.parse(
            request.read_group_ids[0])
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        self.getUserAccessTier(dataset, access_map)
        readGroupSet = dataset.getReadGroupSet(compoundId.read_group_set_id)
        referenceSet = readGroupSet.getReferenceSet()
        if referenceSet is None:
            raise exceptions.ReadGroupSetNotMappedToReferenceSetException(
                readGroupSet.getId())
        reference = referenceSet.getReference(request.reference_id)
        readGroup = readGroupSet.getReadGroup(compoundId.read_group_id)
        intervalIterator = paging.ReadsIntervalIterator(
            request, readGroup, reference)
        return intervalIterator

    def _readsGeneratorMultiple(self, request, access_map):
        compoundId = datamodel.ReadGroupCompoundId.parse(
            request.read_group_ids[0])
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        self.getUserAccessTier(dataset, access_map)
        readGroupSet = dataset.getReadGroupSet(compoundId.read_group_set_id)
        referenceSet = readGroupSet.getReferenceSet()
        if referenceSet is None:
            raise exceptions.ReadGroupSetNotMappedToReferenceSetException(
                readGroupSet.getId())
        reference = referenceSet.getReference(request.reference_id)
        readGroupIds = readGroupSet.getReadGroupIds()
        if set(readGroupIds) != set(request.read_group_ids):
            raise exceptions.BadRequestException(
                "If multiple readGroupIds are specified, "
                "they must be all of the readGroupIds in a ReadGroupSet")
        intervalIterator = paging.ReadsIntervalIterator(
            request, readGroupSet, reference)
        return intervalIterator

    def variantsGenerator(self, request, access_map):
        """
        Returns a generator over the (variant, nextPageToken) pairs defined
        by the specified request.
        """
        variantSetIds = MessageToDict(request).get("variantSetIds", None)
        datasetId = MessageToDict(request).get("datasetId", None)

        # If none of them were specified
        if (datasetId or variantSetIds) is None:
            raise exceptions.BadRequestException("You need to specify one of datasetId or variantSetIds.")

        # If both of them were specified
        if (datasetId and variantSetIds) is not None:
            raise exceptions.BadRequestException("You can only specify one of datasetId or variantSetIds.")

        # When variantSetIds are specified
        if variantSetIds is not None:
            variantSets = []
            for variantsetId in variantSetIds:
                compoundId = datamodel.VariantSetCompoundId.parse(variantsetId)
                dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
                self.getUserAccessTier(dataset, access_map)
                item = dataset.getVariantSet(variantsetId)
                variantSets.append(item)

        # When datasetId is specified, get a list of variantSets associated with it
        else:
            dataset = self.getDataRepository().getDataset(request.dataset_id)
            self.getUserAccessTier(dataset, access_map)
            variantSets = dataset.getVariantSets()
        
        iterators = []

        for item in variantSets:
            iterators.append(list(paging.VariantsIntervalIterator(request, item)))

        return itertools.chain.from_iterable(iterators)

    def genotypeMatrixGenerator(self, request, access_map):
        """
        Returns a generator over the (genotypematrix, nextPageToken) pairs
        defined by the specified request.
        """
        compoundId = datamodel.VariantSetCompoundId \
            .parse(request.variant_set_id)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        self.getUserAccessTier(dataset, access_map)
        variantSet = dataset.getVariantSet(compoundId.variant_set_id)
        intervalIterator = paging.GenotypesIntervalIterator(
            request, variantSet)
        return intervalIterator

    def variantAnnotationsGenerator(self, request, access_map):
        """
        Returns a generator over the (variantAnnotaitons, nextPageToken) pairs
        defined by the specified request.
        """
        compoundId = datamodel.VariantAnnotationSetCompoundId.parse(
            request.variant_annotation_set_id)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        self.getUserAccessTier(dataset, access_map)
        variantSet = dataset.getVariantSet(compoundId.variant_set_id)
        variantAnnotationSet = variantSet.getVariantAnnotationSet(
            request.variant_annotation_set_id)
        iterator = paging.VariantAnnotationsIntervalIterator(
            request, variantAnnotationSet)
        return iterator

    def featuresGenerator(self, request, access_map):
        """
        Returns a generator over the (features, nextPageToken) pairs
        defined by the (JSON string) request.
        """
        compoundId = None
        parentId = None
        if request.feature_set_id != "":
            compoundId = datamodel.FeatureSetCompoundId.parse(
                request.feature_set_id)
        if request.parent_id != "":
            compoundParentId = datamodel.FeatureCompoundId.parse(
                request.parent_id)
            parentId = compoundParentId.featureId
            # A client can optionally specify JUST the (compound) parentID,
            # and the server needs to derive the dataset & featureSet
            # from this (compound) parentID.
            if compoundId is None:
                compoundId = compoundParentId
            else:
                # check that the dataset and featureSet of the parent
                # compound ID is the same as that of the featureSetId
                mismatchCheck = (
                    compoundParentId.dataset_id != compoundId.dataset_id or
                    compoundParentId.feature_set_id !=
                    compoundId.feature_set_id)
                if mismatchCheck:
                    raise exceptions.ParentIncompatibleWithFeatureSet()

        if compoundId is None:
            raise exceptions.FeatureSetNotSpecifiedException()

        dataset = self.getDataRepository().getDataset(
            compoundId.dataset_id)
        self.getUserAccessTier(dataset, access_map)
        featureSet = dataset.getFeatureSet(compoundId.feature_set_id)
        iterator = paging.FeaturesIterator(
            request, featureSet, parentId)
        return iterator

    def continuousGenerator(self, request, access_map):
        """
        Returns a generator over the (continuous, nextPageToken) pairs
        defined by the (JSON string) request.
        """
        compoundId = None
        if request.continuous_set_id != "":
            compoundId = datamodel.ContinuousSetCompoundId.parse(
                request.continuous_set_id)
        if compoundId is None:
            raise exceptions.ContinuousSetNotSpecifiedException()

        dataset = self.getDataRepository().getDataset(
            compoundId.dataset_id)
        # check user acce
        self.getUserAccessTier(dataset, access_map)
        continuousSet = dataset.getContinuousSet(request.continuous_set_id)
        iterator = paging.ContinuousIterator(request, continuousSet)
        return iterator

    def phenotypesGenerator(self, request, access_map):
        """
        Returns a generator over the (phenotypes, nextPageToken) pairs
        defined by the (JSON string) request
        """
        # TODO make paging work using SPARQL?
        compoundId = datamodel.PhenotypeAssociationSetCompoundId.parse(
            request.phenotype_association_set_id)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        self.getUserAccessTier(dataset, access_map)
        phenotypeAssociationSet = dataset.getPhenotypeAssociationSet(
            compoundId.phenotypeAssociationSetId)
        associations = phenotypeAssociationSet.getAssociations(request)
        phenotypes = [association.phenotype for association in associations]
        return self._protocolListGenerator(
            request, phenotypes)

    def genotypesPhenotypesGenerator(self, request, access_map):
        """
        Returns a generator over the (phenotypes, nextPageToken) pairs
        defined by the (JSON string) request
        """
        # TODO make paging work using SPARQL?
        compoundId = datamodel.PhenotypeAssociationSetCompoundId.parse(
            request.phenotype_association_set_id)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        self.getUserAccessTier(dataset, access_map)
        phenotypeAssociationSet = dataset.getPhenotypeAssociationSet(
            compoundId.phenotypeAssociationSetId)
        featureSets = dataset.getFeatureSets()
        annotationList = phenotypeAssociationSet.getAssociations(
            request, featureSets)
        return self._protocolListGenerator(request, annotationList)

    def callSetsGenerator(self, request, access_map):
        """
        Returns a generator over the (callSet, nextPageToken) pairs defined
        by the specified request.
        """
        compoundId = datamodel.VariantSetCompoundId.parse(
            request.variant_set_id)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        self.getUserAccessTier(dataset, access_map)
        variantSet = dataset.getVariantSet(compoundId.variant_set_id)
        results = []
        for obj in variantSet.getCallSets():
            include = True
            if request.name:
                if request.name != obj.getLocalId():
                    include = False
            if request.biosample_id:
                if request.biosample_id != obj.getBiosampleId():
                    include = False
            if include:
                results.append(obj)
        return self._objectListGenerator(request, results)

    def featureSetsGenerator(self, request, access_map):
        """
        Returns a generator over the (featureSet, nextPageToken) pairs
        defined by the specified request.
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        self.getUserAccessTier(dataset, access_map)
        return self._topLevelObjectGenerator(
            request, dataset.getNumFeatureSets(),
            dataset.getFeatureSetByIndex)

    def continuousSetsGenerator(self, request, access_map):
        """
        Returns a generator over the (continuousSet, nextPageToken) pairs
        defined by the specified request.
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        self.getUserAccessTier(dataset, access_map)
        return self._topLevelObjectGenerator(
            request, dataset.getNumContinuousSets(),
            dataset.getContinuousSetByIndex)

    def rnaQuantificationSetsGenerator(self, request, access_map):
        """
        Returns a generator over the (rnaQuantificationSet, nextPageToken)
        pairs defined by the specified request.
        """
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        self.getUserAccessTier(dataset, access_map)
        return self._topLevelObjectGenerator(
            request, dataset.getNumRnaQuantificationSets(),
            dataset.getRnaQuantificationSetByIndex)

    def rnaQuantificationsGenerator(self, request, access_map):
        """
        Returns a generator over the (rnaQuantification, nextPageToken) pairs
        defined by the specified request.
        """
        if len(request.rna_quantification_set_id) < 1:
            raise exceptions.BadRequestException(
                "Rna Quantification Set Id must be specified")
        else:
            compoundId = datamodel.RnaQuantificationSetCompoundId.parse(
                request.rna_quantification_set_id)
            dataset = self.getDataRepository().getDataset(
                compoundId.dataset_id)
            rnaQuantSet = dataset.getRnaQuantificationSet(
                compoundId.rna_quantification_set_id)
        results = []
        for obj in rnaQuantSet.getRnaQuantifications():
            include = True
            if request.biosample_id:
                if request.biosample_id != obj.getBiosampleId():
                    include = False
            if include:
                results.append(obj)
        return self._objectListGenerator(request, results)

    def expressionLevelsGenerator(self, request, access_map):
        """
        Returns a generator over the (expressionLevel, nextPageToken) pairs
        defined by the specified request.

        Currently only supports searching over a specified rnaQuantification
        """
        rnaQuantificationId = request.rna_quantification_id
        compoundId = datamodel.RnaQuantificationCompoundId.parse(
            request.rna_quantification_id)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        self.getUserAccessTier(dataset, access_map)
        rnaQuantSet = dataset.getRnaQuantificationSet(
            compoundId.rna_quantification_set_id)
        rnaQuant = rnaQuantSet.getRnaQuantification(rnaQuantificationId)
        rnaQuantificationId = rnaQuant.getLocalId()
        iterator = paging.ExpressionLevelsIterator(
            request, rnaQuant)
        return iterator

    def peersGenerator(self, request, access_map):
        """
        Returns a generator over the (peer, nextPageToken) pairs
        defined by the specified request.
        """
        return paging.PeerIterator(
            request,
            self.getDataRepository())

    #    #
    # Public API methods. Each of these methods implements the
    # corresponding API end point, and return data ready to be
    # written to the wire.
    #
    #
    def runGetRequest(self, obj, return_mimetype="application/json", tier=0):
        """
        Runs a get request by converting the specified datamodel
        object into its protocol representation.
        """
        protocolElement = obj.toProtocolElement(tier=tier)
        data = protocol.serialize(protocolElement, return_mimetype)
        return data

    def runSearchRequest(
            self, requestStr, requestClass, responseClass, objectGenerator,
            access_map, return_mimetype="application/json"):
        """
        Runs the specified request. The request is a string containing
        a JSON representation of an instance of the specified requestClass.
        We return a string representation of an instance of the
        specified responseClass in return_mimetype format. Objects
        are filled into the page list using the specified object
        generator, which must return (object, nextPageToken) pairs,
        and be able to resume iteration from any point using the
        nextPageToken attribute of the request object.
        """
        self.startProfile()
        try:
            request = protocol.fromJson(requestStr, requestClass)
        except protocol.json_format.ParseError:
            raise exceptions.InvalidJsonException(requestStr)
        # TODO How do we detect when the page size is not set?
        if not request.page_size:
            request.page_size = self._defaultPageSize
        if request.page_size < 0:
            raise exceptions.BadPageSizeException(request.page_size)
        responseBuilder = response_builder.SearchResponseBuilder(
            responseClass, request.page_size, self._maxResponseLength,
            return_mimetype)
        nextPageToken = None
        for obj, nextPageToken in objectGenerator(request, access_map):
            responseBuilder.addValue(obj)
            if responseBuilder.isFull():
                break
        responseBuilder.setNextPageToken(nextPageToken)
        responseString = responseBuilder.getSerializedResponse()
        self.endProfile()
        return responseString

    def runListReferenceBases(self, requestJson,
                              return_mimetype="application/json"):
        """
        Runs a listReferenceBases request for the specified ID and
        request arguments.
        """
        # In the case when an empty post request is made to the endpoint
        # we instantiate an empty ListReferenceBasesRequest.
        if not requestJson:
            request = protocol.ListReferenceBasesRequest()
        else:
            try:
                request = protocol.fromJson(
                    requestJson,
                    protocol.ListReferenceBasesRequest)
            except protocol.json_format.ParseError:
                raise exceptions.InvalidJsonException(requestJson)
        compoundId = datamodel.ReferenceCompoundId.parse(request.reference_id)
        referenceSet = self.getDataRepository().getReferenceSet(
            compoundId.reference_set_id)
        reference = referenceSet.getReference(request.reference_id)
        start = request.start
        end = request.end
        if end == 0:  # assume meant "get all"
            end = reference.getLength()
        if request.page_token:
            pageTokenStr = request.page_token
            start = paging._parsePageToken(pageTokenStr, 1)[0]

        chunkSize = self._maxResponseLength
        nextPageToken = None
        if start + chunkSize < end:
            end = start + chunkSize
            nextPageToken = str(start + chunkSize)
        sequence = reference.getBases(start, end)

        # build response
        response = protocol.ListReferenceBasesResponse()
        response.offset = start
        response.sequence = sequence
        if nextPageToken:
            response.next_page_token = nextPageToken
        return protocol.serialize(response, return_mimetype)

    def runSearchGenotypesRequest(self, requestStr, access_map,
                                  return_mimetype="application/json"):
        """
        Runs a searchGenotypes request for the specified
        request arguments.

        Can't just use runSearchRequest because we're appending
        multiple things - the variants and the genotype matrix
        """
        self.startProfile()
        requestClass = protocol.SearchGenotypesRequest
        responseClass = protocol.SearchGenotypesResponse
        objectGenerator = self.genotypeMatrixGenerator

        try:
            request = protocol.fromJson(requestStr, requestClass)
        except protocol.json_format.ParseError:
            raise exceptions.InvalidJsonException(requestStr)

        response = responseClass()
        response.genotypes.nvariants = 0
        response.genotypes.nindividuals = 0

        # to heck with paging for now
        # and to heck with call set ids too

        genotyperows = []
        variants = []
        callsetIds = None
        for gt_variant, nextPageToken in objectGenerator(request, access_map):
            genotypemtx, variant, callsetids = gt_variant
            genotyperows.append(genotypemtx)
            variant.ClearField(b"calls")
            variants.append(variant)
            if callsetIds is None:
                callsetIds = callsetids

        for genotyperow in genotyperows:
            response.genotypes.genotypes.extend(genotyperow.genotypes)
        response.genotypes.nindividuals = len(genotyperows[0].genotypes)
        response.genotypes.nvariants = len(variants)

        response.variants.extend(variants)
        response.call_set_ids.extend(callsetIds)

        return protocol.serialize(response, return_mimetype)

    # Get requests.

    def runGetCallSet(self, id_, access_map, return_mimetype="application/json"):
        """
        Returns a callset with the given id
        """
        compoundId = datamodel.CallSetCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        variantSet = dataset.getVariantSet(compoundId.variant_set_id)
        callSet = variantSet.getCallSet(id_)
        return self.runGetRequest(callSet, return_mimetype, tier=tier)

    def runGetInfo(self, request, return_mimetype="application/json"):
        """
        Returns information about the service including protocol version.
        """
        return protocol.serialize(protocol.GetInfoResponse(
            protocol_version=protocol.version), return_mimetype)

    def runAddAnnouncement(self, flaskrequest):
        """
        Takes a flask request from the frontend and attempts to parse
        into an AnnouncePeerRequest. If successful, it will log the
        announcement to the `announcement` table with some other metadata
        gathered from the request.
        """
        announcement = {}
        # We want to parse the request ourselves to collect a little more
        # data about it.
        try:
            requestData = protocol.fromJson(
                flaskrequest.get_data(), protocol.AnnouncePeerRequest)
            announcement['hostname'] = flaskrequest.host_url
            announcement['remote_addr'] = flaskrequest.remote_addr
            announcement['user_agent'] = flaskrequest.headers.get('User-Agent')
        except AttributeError:
            # Sometimes in testing we will send protocol requests instead
            # of flask requests and so the hostname and user agent won't
            # be present.
            try:
                requestData = protocol.fromJson(
                    flaskrequest, protocol.AnnouncePeerRequest)
            except Exception as e:
                raise exceptions.InvalidJsonException(e)
        except Exception as e:
            raise exceptions.InvalidJsonException(e)

        # Validate the url before accepting the announcement
        peer = datamodel.peers.Peer(requestData.peer.url)
        peer.setAttributesJson(protocol.toJson(
            requestData.peer.attributes))
        announcement['url'] = peer.getUrl()
        announcement['attributes'] = peer.getAttributes()
        try:
            self.getDataRepository().insertAnnouncement(announcement)
        except:
            raise exceptions.BadRequestException(announcement['url'])
        return protocol.toJson(
            protocol.AnnouncePeerResponse(success=True))

    def runListPeers(self, request, access_map):
        """
        Takes a ListPeersRequest and returns a ListPeersResponse using
        a page_token and page_size if provided.
        """
        return self.runSearchRequest(
            request,
            protocol.ListPeersRequest,
            protocol.ListPeersResponse,
            access_map,
            self.peersGenerator
        )

    def runGetVariant(self, id_, access_map, return_mimetype="application/json"):
        """
        Returns a variant with the given id
        """
        compoundId = datamodel.VariantCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        # tier = self.getUserAccessTier(dataset, access_map)
        variantSet = dataset.getVariantSet(compoundId.variant_set_id)
        gaVariant = variantSet.getVariant(compoundId)
        # TODO variant is a special case here, as it's returning a
        # protocol element rather than a datamodel object. We should
        # fix this for consistency.
        data = protocol.serialize(gaVariant, return_mimetype)
        return data

    def runGetBiosample(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getBiosample request for the specified ID.
        """
        compoundId = datamodel.BiosampleCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        biosample = dataset.getBiosample(id_)
        return self.runGetRequest(biosample, return_mimetype, tier=tier)

    def runGetIndividual(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getIndividual request for the specified ID.
        """
        compoundId = datamodel.BiosampleCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        individual = dataset.getIndividual(id_)
        return self.runGetRequest(individual, return_mimetype, tier=tier)

    def runGetPatient(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getPatient request for the specified ID.
        """
        compoundId = datamodel.PatientCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        patient = dataset.getPatient(id_)
        return self.runGetRequest(patient, return_mimetype, tier=tier)

    def runGetEnrollment(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getEnrollment request for the specified ID.
        """
        compoundId = datamodel.EnrollmentCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        enrollment = dataset.getEnrollment(id_)
        return self.runGetRequest(enrollment, return_mimetype, tier=tier)

    def runGetConsent(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getConsent request for the specified ID.
        """
        compoundId = datamodel.ConsentCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        consent = dataset.getConsent(id_)
        return self.runGetRequest(consent, return_mimetype, tier=tier)

    def runGetDiagnosis(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getDiagnosis request for the specified ID.
        """
        compoundId = datamodel.DiagnosisCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        diagnosis = dataset.getDiagnosis(id_)
        return self.runGetRequest(diagnosis, return_mimetype, tier=tier)

    def runGetSample(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getSample request for the specified ID.
        """
        compoundId = datamodel.SampleCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        sample = dataset.getSample(id_)
        return self.runGetRequest(sample, return_mimetype, tier=tier)

    def runGetTreatment(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getTreatment request for the specified ID.
        """
        compoundId = datamodel.TreatmentCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        treatment = dataset.getTreatment(id_)
        return self.runGetRequest(treatment, return_mimetype, tier=tier)

    def runGetOutcome(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getOutcome request for the specified ID.
        """
        compoundId = datamodel.OutcomeCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        outcome = dataset.getOutcome(id_)
        return self.runGetRequest(outcome, return_mimetype, tier=tier)

    def runGetComplication(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getComplication request for the specified ID.
        """
        compoundId = datamodel.ComplicationCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        complication = dataset.getComplication(id_)
        return self.runGetRequest(complication, return_mimetype, tier=tier)

    def runGetTumourboard(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getTumourboard request for the specified ID.
        """
        compoundId = datamodel.TumourboardCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        tumourboard = dataset.getTumourboard(id_)
        return self.runGetRequest(tumourboard, return_mimetype, tier=tier)

    def runGetChemotherapy(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getChemotherapy request for the specified ID.
        """
        compoundId = datamodel.BiosampleCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        chemotherapy = dataset.getChemotherapy(id_)
        return self.runGetRequest(chemotherapy, return_mimetype, tier=tier)

    def runGetRadiotherapy(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getRadiotherapy request for the specified ID.
        """
        compoundId = datamodel.BiosampleCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        radiotherapy = dataset.getRadiotherapy(id_)
        return self.runGetRequest(radiotherapy, return_mimetype, tier=tier)

    def runGetSurgery(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getSurgery request for the specified ID.
        """
        compoundId = datamodel.BiosampleCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        surgery = dataset.getSurgery(id_)
        return self.runGetRequest(surgery, return_mimetype, tier=tier)

    def runGetImmunotherapy(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getImmunotherapy request for the specified ID.
        """
        compoundId = datamodel.BiosampleCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        immunotherapy = dataset.getImmunotherapy(id_)
        return self.runGetRequest(immunotherapy, return_mimetype, tier=tier)

    def runGetCelltransplant(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getCelltransplant request for the specified ID.
        """
        compoundId = datamodel.BiosampleCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        celltransplant = dataset.getCelltransplant(id_)
        return self.runGetRequest(celltransplant, return_mimetype, tier=tier)

    def runGetSlide(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getSlide request for the specified ID.
        """
        compoundId = datamodel.BiosampleCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        slide = dataset.getSlide(id_)
        return self.runGetRequest(slide, return_mimetype, tier=tier)

    def runGetStudy(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getStudy request for the specified ID.
        """
        compoundId = datamodel.BiosampleCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        study = dataset.getStudy(id_)
        return self.runGetRequest(study, return_mimetype, tier=tier)

    def runGetLabtest(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getLabtest request for the specified ID.
        """
        compoundId = datamodel.BiosampleCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        labtest = dataset.getLabtest(id_)
        return self.runGetRequest(labtest, return_mimetype, tier=tier)

    def runGetExtraction(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getExtraction request for the specified ID.
        """
        compoundId = datamodel.ExtractionCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        extraction = dataset.getExtraction(id_)
        return self.runGetRequest(extraction, return_mimetype, tier=tier)

    def runGetSequencing(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getSample request for the specified ID.
        """
        compoundId = datamodel.SequencingCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        sequencing = dataset.getSequencing(id_)
        return self.runGetRequest(sequencing, return_mimetype, tier=tier)

    def runGetAlignment(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getAlignment request for the specified ID.
        """
        compoundId = datamodel.AlignmentCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        alignment = dataset.getAlignment(id_)
        return self.runGetRequest(alignment, return_mimetype, tier=tier)

    def runGetVariantCalling(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getVariantCalling request for the specified ID.
        """
        compoundId = datamodel.VariantCallingCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        variantCalling = dataset.getVariantCalling(id_)
        return self.runGetRequest(variantCalling, return_mimetype, tier=tier)

    def runGetFusionDetection(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getFusionDetection request for the specified ID.
        """
        compoundId = datamodel.FusionDetectionCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        fusionDetection = dataset.getFusionDetection(id_)
        return self.runGetRequest(fusionDetection, return_mimetype, tier=tier)

    def runGetExpressionAnalysis(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getExpressionAnalyis request for the specified ID.
        """
        compoundId = datamodel.ExpressionAnalysisCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        expressionAnalysis = dataset.getExpressionAnalysis(id_)
        return self.runGetRequest(expressionAnalysis, return_mimetype, tier=tier)

    def runGetFeature(self, id_, access_map, return_mimetype="application/json"):
        """
        Returns JSON string of the feature object corresponding to
        the feature compoundID passed in.
        """
        compoundId = datamodel.FeatureCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        # tier = self.getUserAccessTier(dataset, access_map)
        featureSet = dataset.getFeatureSet(compoundId.feature_set_id)
        gaFeature = featureSet.getFeature(compoundId)
        data = protocol.serialize(gaFeature, return_mimetype)
        return data

    def runGetReadGroupSet(self, id_, access_map, return_mimetype="application/json"):
        """
        Returns a readGroupSet with the given id_
        """
        compoundId = datamodel.ReadGroupSetCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        readGroupSet = dataset.getReadGroupSet(id_)
        return self.runGetRequest(readGroupSet, return_mimetype, tier=tier)

    def runGetReadGroup(self, id_, access_map, return_mimetype="application/json"):
        """
        Returns a read group with the given id_
        """
        compoundId = datamodel.ReadGroupCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        readGroupSet = dataset.getReadGroupSet(compoundId.read_group_set_id)
        readGroup = readGroupSet.getReadGroup(id_)
        return self.runGetRequest(readGroup, return_mimetype, tier=tier)

    def runGetReference(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getReference request for the specified ID.
        """
        compoundId = datamodel.ReferenceCompoundId.parse(id_)
        referenceSet = self.getDataRepository().getReferenceSet(
            compoundId.reference_set_id)
        reference = referenceSet.getReference(id_)
        return self.runGetRequest(reference, return_mimetype, tier=0)

    def runGetReferenceSet(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getReferenceSet request for the specified ID.
        """
        referenceSet = self.getDataRepository().getReferenceSet(id_)
        return self.runGetRequest(referenceSet, return_mimetype, tier=0)

    def runGetVariantSet(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getVariantSet request for the specified ID.
        """
        compoundId = datamodel.VariantSetCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        variantSet = dataset.getVariantSet(id_)
        return self.runGetRequest(variantSet, return_mimetype, tier=tier)

    def runGetFeatureSet(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getFeatureSet request for the specified ID.
        """
        compoundId = datamodel.FeatureSetCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        featureSet = dataset.getFeatureSet(id_)
        return self.runGetRequest(featureSet, return_mimetype, tier=tier)

    def runGetContinuousSet(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getContinuousSet request for the specified ID.
        """
        compoundId = datamodel.ContinuousSetCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        continuousSet = dataset.getContinuousSet(id_)
        return self.runGetRequest(continuousSet, return_mimetype, tier=tier)

    def runGetDataset(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getDataset request for the specified ID.
        """
        dataset = self.getDataRepository().getDataset(id_)
        tier = self.getUserAccessTier(dataset, access_map)
        return self.runGetRequest(dataset, return_mimetype, tier=tier)

    def runGetExperiment(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getExperiment request for the specified ID.
        """
        experiment = self.getDataRepository().getExperiment(id_)
        return self.runGetRequest(experiment, return_mimetype, tier=0)

    def runGetAnalysis(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getAnalysis request for the specified ID.
        """
        analysis = self.getDataRepository().getAnalysis(id_)
        return self.runGetRequest(analysis, return_mimetype, tier=0)

    def runGetVariantAnnotationSet(self, id_, access_map,
                                   return_mimetype="application/json"):
        """
        Runs a getVariantSet request for the specified ID.
        """
        compoundId = datamodel.VariantAnnotationSetCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        variantSet = dataset.getVariantSet(compoundId.variant_set_id)
        variantAnnotationSet = variantSet.getVariantAnnotationSet(id_)
        return self.runGetRequest(variantAnnotationSet, return_mimetype, tier=tier)

    def runGetRnaQuantification(self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getRnaQuantification request for the specified ID.
        """
        compoundId = datamodel.RnaQuantificationCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        rnaQuantificationSet = dataset.getRnaQuantificationSet(
            compoundId.rna_quantification_set_id)
        rnaQuantification = rnaQuantificationSet.getRnaQuantification(id_)
        return self.runGetRequest(rnaQuantification, return_mimetype, tier=tier)

    def runGetRnaQuantificationSet(self, id_, access_map,
                                   return_mimetype="application/json"):
        """
        Runs a getRnaQuantificationSet request for the specified ID.
        """
        compoundId = datamodel.RnaQuantificationSetCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        rnaQuantificationSet = dataset.getRnaQuantificationSet(id_)
        return self.runGetRequest(rnaQuantificationSet, return_mimetype, tier=tier)

    def runGetExpressionLevel(
            self, id_, access_map, return_mimetype="application/json"):
        """
        Runs a getExpressionLevel request for the specified ID.
        """
        compoundId = datamodel.ExpressionLevelCompoundId.parse(id_)
        dataset = self.getDataRepository().getDataset(compoundId.dataset_id)
        tier = self.getUserAccessTier(dataset, access_map)
        rnaQuantificationSet = dataset.getRnaQuantificationSet(
            compoundId.rna_quantification_set_id)
        rnaQuantification = rnaQuantificationSet.getRnaQuantification(
            compoundId.rna_quantification_id)
        expressionLevel = rnaQuantification.getExpressionLevel(compoundId)
        return self.runGetRequest(expressionLevel, return_mimetype, tier=tier)

    # Search requests.

    def runSearchReadGroupSets(self, request, return_mimetype, access_map):
        """
        Runs the specified SearchReadGroupSetsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchReadGroupSetsRequest,
            protocol.SearchReadGroupSetsResponse,
            self.readGroupSetsGenerator,
            access_map,
            return_mimetype)

    def runSearchIndividuals(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchIndividualsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchIndividualsRequest,
            protocol.SearchIndividualsResponse,
            self.individualsGenerator,
            access_map,
            return_mimetype)

    # Search requests
    def runSearchQuery(self, request, return_mimetype, access_map):
        """
        Runs advanced SearchRequest
        """
        try:
            request = protocol.fromJson(request, protocol.SearchQueryRequest)
        except protocol.json_format.ParseError as e:
            raise exceptions.InvalidJsonException(str(e))
        return self.queryGenerator(request, return_mimetype, access_map)

    # Count requests
    def runCountQuery(self, request, return_mimetype, access_map):
        """
        Runs count query on top of advanced SearchRequest
        """
        try:
            request = protocol.fromJson(request, protocol.SearchQueryRequest)
        except protocol.json_format.ParseError as e:
            raise exceptions.InvalidJsonException(str(e))
        return self.queryGenerator(request, return_mimetype, access_map, count=True)

    def runSearchPatients(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchPatientsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchPatientsRequest,
            protocol.SearchPatientsResponse,
            self.patientsGenerator,
            access_map,
            return_mimetype,
        )

    def runSearchEnrollments(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchEnrollmentsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchEnrollmentsRequest,
            protocol.SearchEnrollmentsResponse,
            self.enrollmentsGenerator,
            access_map,
            return_mimetype
        )

    def runSearchConsents(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchConsentsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchConsentsRequest,
            protocol.SearchConsentsResponse,
            self.consentsGenerator,
            access_map,
            return_mimetype
        )

    def runSearchDiagnoses(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchDiagnosesRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchDiagnosesRequest,
            protocol.SearchDiagnosesResponse,
            self.diagnosesGenerator,
            access_map,
            return_mimetype
        )

    def runSearchSamples(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchSamplesRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchSamplesRequest,
            protocol.SearchSamplesResponse,
            self.samplesGenerator,
            access_map,
            return_mimetype
        )

    def runSearchTreatments(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchTreatmentsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchTreatmentsRequest,
            protocol.SearchTreatmentsResponse,
            self.treatmentsGenerator,
            access_map,
            return_mimetype
        )

    def runSearchOutcomes(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchOutcomesRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchOutcomesRequest,
            protocol.SearchOutcomesResponse,
            self.outcomesGenerator,
            access_map,
            return_mimetype
        )

    def runSearchComplications(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchComplicationsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchComplicationsRequest,
            protocol.SearchComplicationsResponse,
            self.complicationsGenerator,
            access_map,
            return_mimetype
        )

    def runSearchTumourboards(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchTumourboardsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchTumourboardsRequest,
            protocol.SearchTumourboardsResponse,
            self.tumourboardsGenerator,
            access_map,
            return_mimetype
        )

    def runSearchChemotherapies(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchChemotherapiesRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchChemotherapiesRequest,
            protocol.SearchChemotherapiesResponse,
            self.chemotherapiesGenerator,
            access_map,
            return_mimetype)

    def runSearchRadiotherapies(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchRadiotherapiesRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchRadiotherapiesRequest,
            protocol.SearchRadiotherapiesResponse,
            self.radiotherapiesGenerator,
            access_map,
            return_mimetype)

    def runSearchSurgeries(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchSurgeriesRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchSurgeriesRequest,
            protocol.SearchSurgeriesResponse,
            self.surgeriesGenerator,
            access_map,
            return_mimetype)

    def runSearchImmunotherapies(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchImmunotherapiesRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchImmunotherapiesRequest,
            protocol.SearchImmunotherapiesResponse,
            self.immunotherapiesGenerator,
            access_map,
            return_mimetype)

    def runSearchCelltransplants(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchCelltransplantsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchCelltransplantsRequest,
            protocol.SearchCelltransplantsResponse,
            self.celltransplantsGenerator,
            access_map,
            return_mimetype)

    def runSearchSlides(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchSlidesRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchSlidesRequest,
            protocol.SearchSlidesResponse,
            self.slidesGenerator,
            access_map,
            return_mimetype)

    def runSearchStudies(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchStudiesRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchStudiesRequest,
            protocol.SearchStudiesResponse,
            self.studiesGenerator,
            access_map,
            return_mimetype)

    def runSearchLabtests(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchLabtestsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchLabtestsRequest,
            protocol.SearchLabtestsResponse,
            self.labtestsGenerator,
            access_map,
            return_mimetype)

    def runSearchExtractions(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchExtractionsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchExtractionsRequest,
            protocol.SearchExtractionsResponse,
            self.extractionsGenerator,
            access_map,
            return_mimetype
        )

    def runSearchSequencing(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchSequencingRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchSequencingRequest,
            protocol.SearchSequencingResponse,
            self.sequencingGenerator,
            access_map,
            return_mimetype
        )

    def runSearchAlignments(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchAlignmentsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchAlignmentsRequest,
            protocol.SearchAlignmentsResponse,
            self.alignmentsGenerator,
            access_map,
            return_mimetype
        )

    def runSearchVariantCalling(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchVariantCallingRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchVariantCallingRequest,
            protocol.SearchVariantCallingResponse,
            self.variantCallingGenerator,
            access_map,
            return_mimetype
        )

    def runSearchFusionDetection(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchFusionDetectionRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchFusionDetectionRequest,
            protocol.SearchFusionDetectionResponse,
            self.fusionDetectionGenerator,
            access_map,
            return_mimetype
        )

    def runSearchExpressionAnalysis(self, request, return_mimetype, access_map):
        """
        Runs the specified search SearchExpressionAnalysisRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchExpressionAnalysisRequest,
            protocol.SearchExpressionAnalysisResponse,
            self.expressionAnalysisGenerator,
            access_map,
            return_mimetype
        )

    def runSearchBiosamples(self, request, return_mimetype, access_map):
        """
        Runs the specified SearchBiosamplesRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchBiosamplesRequest,
            protocol.SearchBiosamplesResponse,
            self.biosamplesGenerator,
            access_map,
            return_mimetype)

    def runSearchReads(self, request, return_mimetype, access_map):
        """
        Runs the specified SearchReadsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchReadsRequest,
            protocol.SearchReadsResponse,
            self.readsGenerator,
            access_map,
            return_mimetype)

    def runSearchReferenceSets(self, request, return_mimetype, access_map):
        """
        Runs the specified SearchReferenceSetsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchReferenceSetsRequest,
            protocol.SearchReferenceSetsResponse,
            self.referenceSetsGenerator,
            access_map,
            return_mimetype)

    def runSearchReferences(self, request, return_mimetype, access_map):
        """
        Runs the specified SearchReferenceRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchReferencesRequest,
            protocol.SearchReferencesResponse,
            self.referencesGenerator,
            access_map,
            return_mimetype)

    def runSearchVariantSets(self, request, return_mimetype, access_map):
        """
        Runs the specified SearchVariantSetsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchVariantSetsRequest,
            protocol.SearchVariantSetsResponse,
            self.variantSetsGenerator,
            access_map,
            return_mimetype)

    def runSearchVariantAnnotationSets(self, request, return_mimetype, access_map):
        """
        Runs the specified SearchVariantAnnotationSetsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchVariantAnnotationSetsRequest,
            protocol.SearchVariantAnnotationSetsResponse,
            self.variantAnnotationSetsGenerator,
            access_map,
            return_mimetype)

    def runSearchVariants(self, request, return_mimetype, access_map):
        """
        Runs the specified SearchVariantRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchVariantsRequest,
            protocol.SearchVariantsResponse,
            self.variantsGenerator,
            access_map,
            return_mimetype)

    def runSearchGenotypes(self, request, return_mimetype, access_map):
        """
        Runs the specified SearchVariantRequest.
        """
        return self.runSearchGenotypesRequest(request, access_map, return_mimetype)

    def runSearchVariantAnnotations(self, request, return_mimetype, access_map):
        """
        Runs the specified SearchVariantAnnotationsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchVariantAnnotationsRequest,
            protocol.SearchVariantAnnotationsResponse,
            self.variantAnnotationsGenerator,
            access_map,
            return_mimetype)

    def runSearchCallSets(self, request, return_mimetype, access_map):
        """
        Runs the specified SearchCallSetsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchCallSetsRequest,
            protocol.SearchCallSetsResponse,
            self.callSetsGenerator,
            access_map,
            return_mimetype)

    def runSearchDatasets(self, request, return_mimetype, access_map):
        """
        Runs the specified SearchDatasetsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchDatasetsRequest,
            protocol.SearchDatasetsResponse,
            self.datasetsGenerator,
            access_map,
            return_mimetype)

    def runSearchExperiments(self, request, return_mimetype, access_map):
        """
        Runs the specified SearchExperimentsRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchExperimentsRequest,
            protocol.SearchExperimentsResponse,
            self.experimentsGenerator,
            access_map,
            return_mimetype)

    def runSearchAnalyses(self, request, return_mimetype, access_map):
        """
        Runs the specified SearchAnalysesRequest.
        """
        return self.runSearchRequest(
            request, protocol.SearchAnalysesRequest,
            protocol.SearchAnalysesResponse,
            self.analysesGenerator,
            access_map,
            return_mimetype)

    def runSearchFeatureSets(self, request, return_mimetype, access_map):
        """
        Returns a SearchFeatureSetsResponse for the specified
        SearchFeatureSetsRequest object.
        """
        return self.runSearchRequest(
            request, protocol.SearchFeatureSetsRequest,
            protocol.SearchFeatureSetsResponse,
            self.featureSetsGenerator,
            access_map,
            return_mimetype)

    def runSearchFeatures(self, request, return_mimetype, access_map):
        """
        Returns a SearchFeaturesResponse for the specified
        SearchFeaturesRequest object.

        :param request: JSON string representing searchFeaturesRequest
        :return: JSON string representing searchFeatureResponse
        """
        return self.runSearchRequest(
            request, protocol.SearchFeaturesRequest,
            protocol.SearchFeaturesResponse,
            self.featuresGenerator,
            access_map,
            return_mimetype)

    def runSearchContinuousSets(self, request, return_mimetype, access_map):
        """
        Returns a SearchContinuousSetsResponse for the specified
        SearchContinuousSetsRequest object.
        """
        return self.runSearchRequest(
            request, protocol.SearchContinuousSetsRequest,
            protocol.SearchContinuousSetsResponse,
            self.continuousSetsGenerator,
            access_map,
            return_mimetype)

    def runSearchContinuous(self, request, return_mimetype, access_map):
        """
        Returns a SearchContinuousResponse for the specified
        SearchContinuousRequest object.

        :param request: JSON string representing searchContinuousRequest
        :return: JSON string representing searchContinuousResponse
        """
        return self.runSearchRequest(
            request, protocol.SearchContinuousRequest,
            protocol.SearchContinuousResponse,
            self.continuousGenerator,
            access_map,
            return_mimetype)

    def runSearchGenotypePhenotypes(self, request, return_mimetype, access_map):
        return self.runSearchRequest(
            request, protocol.SearchGenotypePhenotypeRequest,
            protocol.SearchGenotypePhenotypeResponse,
            self.genotypesPhenotypesGenerator,
            access_map,
            return_mimetype)

    def runSearchPhenotypes(self, request, return_mimetype, access_map):
        return self.runSearchRequest(
            request, protocol.SearchPhenotypesRequest,
            protocol.SearchPhenotypesResponse,
            self.phenotypesGenerator,
            access_map,
            return_mimetype)

    def runSearchPhenotypeAssociationSets(self, request, return_mimetype, access_map):
        return self.runSearchRequest(
            request, protocol.SearchPhenotypeAssociationSetsRequest,
            protocol.SearchPhenotypeAssociationSetsResponse,
            self.phenotypeAssociationSetsGenerator,
            access_map,
            return_mimetype)

    def runSearchRnaQuantificationSets(self, request, return_mimetype, access_map):
        """
        Returns a SearchRnaQuantificationSetsResponse for the specified
        SearchRnaQuantificationSetsRequest object.
        """
        return self.runSearchRequest(
            request, protocol.SearchRnaQuantificationSetsRequest,
            protocol.SearchRnaQuantificationSetsResponse,
            self.rnaQuantificationSetsGenerator,
            access_map,
            return_mimetype)

    def runSearchRnaQuantifications(self, request, return_mimetype, access_map):
        """
        Returns a SearchRnaQuantificationResponse for the specified
        SearchRnaQuantificationRequest object.
        """
        return self.runSearchRequest(
            request, protocol.SearchRnaQuantificationsRequest,
            protocol.SearchRnaQuantificationsResponse,
            self.rnaQuantificationsGenerator,
            access_map,
            return_mimetype)

    def runSearchExpressionLevels(self, request, return_mimetype, access_map):
        """
        Returns a SearchExpressionLevelResponse for the specified
        SearchExpressionLevelRequest object.
        """
        return self.runSearchRequest(
            request, protocol.SearchExpressionLevelsRequest,
            protocol.SearchExpressionLevelsResponse,
            self.expressionLevelsGenerator,
            access_map,
            return_mimetype)

    def runSearchVariantsByGeneName(self, request, return_mimetype, access_map):
        """
        Returns a SearchVariantsByGeneNameResponse for the specified
        SearchVariantsByGeneNameRequest object.
        """
        return self.runSearchRequest(
            request, protocol.SearchVariantsByGeneNameRequest,
            protocol.SearchVariantsByGeneNameResponse,
            self.runSearchVariantsByGeneNameGenerator,
            access_map,
            return_mimetype)

    def runSearchVariantsByGeneNameGenerator(self, request, access_map):
        """
        Returns a generator over the geneName
        defined by the specified request.
        """
        results = []
        processedVariantsets = []
        dataset = self.getDataRepository().getDataset(request.dataset_id)
        self.getUserAccessTier(dataset, access_map)
        variantsets = dataset.getVariantSets()
        patientList = MessageToDict(request).get("patientList", None)

        if patientList is None:
            processedVariantsets = variantsets
        else:
            for variantset in variantsets:
                if variantset.getPatientId() in patientList:
                    processedVariantsets.append(variantset)

        if request.gene == "" and (request.start == 0 or request.end == 0 or request.reference_name == ""):
            raise exceptions.BadRequestException("You have to specify a gene.")

        if request.gene != "":
            for featureset in dataset.getFeatureSets():
                for feature in featureset.getFeatures(geneSymbol=request.gene):
                    for variantset in processedVariantsets:
                        for variant in variantset.getVariants(
                                referenceName=feature.reference_name.replace('chr', ''),
                                startPosition=feature.start,
                                endPosition=feature.end,
                        ):
                            if patientList is not None:
                                setattr(variant, "patientId", variantset.getPatientId())
                            results.append(variant)

        elif request.start != "":
            iterators = []
            for item in processedVariantsets:
                iterators.append(list(paging.VariantsIntervalIterator(request, item)))

            return itertools.chain.from_iterable(iterators)

        return self._protocolListGenerator(request, results)

    def getUserAccessTier(self, dataset, access_map):
        """
        :param dataset: dataset object
        :param access_map: dict mapping the authenticated users groups to access tiers
        :return: an access tier for a given dataset
        """
        dataset_name = dataset.getLocalId()

        if dataset_name in access_map:
            return int(access_map[dataset_name])
        else:
            raise exceptions.NotAuthorizedException("Not authorized to access this dataset")

    def _topLevelAuthzDatasetGenerator(self, request, numObjects, getDatasetMethod, access_map=None):
        """
        top level authorized object generator to use with access maps (e.g. datasets/search)
        """
        if not access_map:
            access_map = {}
        currentIndex = 0
        while currentIndex < numObjects:
            object_ = getDatasetMethod(currentIndex, access_map)
            currentIndex += 1
            if object_:
                yield object_.toProtocolElement(0), None
