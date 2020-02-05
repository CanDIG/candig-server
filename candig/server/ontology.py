import json
import warnings
from datetime import datetime

import candig.server.exceptions as exceptions

from pronto import Ontology


class OntologyFile():
    """
    Get a list of ontology terms of an ontology file.

    Example usage:

    from pronto import Ontology
    ont = Ontology("https://raw.githubusercontent.com/EBISPOT/DUO/master/src/ontology/duo-basic.owl")
    duos = OntologyFile(ont)
    duo_terms = duos.get_terms()
    """

    def __init__(self, ont):
        """
        ont
        """
        self.ontology_file_object = ont

    def get_terms(self):
        res = []

        for term in self.ontology_file_object.terms():
            obj = {}
            obj['id'] = term.id
            obj['name'] = term.name
            res.append(obj)

        return res


class OntologyParser():
    """
    This class provides methods to get the attributes of an ontology term.

    Example usage:

    from pronto import Ontology
    ont = Ontology("https://raw.githubusercontent.com/EBISPOT/DUO/master/src/ontology/duo-basic.owl")
    duo = OntologyParser(ont, "DUO:0000025")
    term_overview = duo.get_overview()
    """

    def __init__(self, ont, term_id):
        self.ontology_term_object = ont[term_id]
        self.shorthand_prop = "http://www.geneontology.org/formats/oboInOwl#shorthand"

    def get_term_id(self):
        return self.ontology_term_object.id

    def get_shorthand(self):
        annotations = self.ontology_term_object.annotations
        return next((pv.literal for pv in annotations if pv.property == self.shorthand_prop), None)

    def get_name(self):
        return self.ontology_term_object.name

    def get_definition(self):
        return str(self.ontology_term_object.definition)

    def get_comment(self):
        return self.ontology_term_object.comment

    def get_relationships(self):
        relationships = self.ontology_term_object.relationships
        res = {}

        for rel_key in relationships:
            res[rel_key.id] = next(iter(relationships[rel_key])).id

        return res

    def get_overview(self):
        res = {}
        res["shorthand"] = self.get_shorthand()
        res["name"] = self.get_name()
        res["definition"] = self.get_definition()
        res["relationships"] = self.get_relationships()

        return res


class OntologyValidator():
    """
    Validate a json file that contains Data Use Ontology information.
    The file should be formatted as {"duo": []}, with the value being a list of DUO objects.
    All DUO objects must contain an 'id' field, selected 'id's need to have 'modifier'.

    Example input file:

    {"duo": [{"id": "DUO:0000018"}, {"id": "DUO:0000025", "modifier": "2030-01-01"}]}

    Example Usage:

    with open("duo.json", 'r') as f:
        validator = OntologyValidator(f)

    if validator.validate_duo():
        terms = validator.get_duo_list()

    """

    def __init__(self, input_json):
        self.input_json = input_json
        self.ids_require_datetime_modifier = ["DUO:0000024"]
        self.ids_supported = [
            "DUO:0000001", "DUO:0000004",
            "DUO:0000005", "DUO:0000006", "DUO:0000007", "DUO:0000011",
            "DUO:0000012", "DUO:0000014", "DUO:0000015", "DUO:0000016",
            "DUO:0000017", "DUO:0000018", "DUO:0000019", "DUO:0000020",
            "DUO:0000021", "DUO:0000024", "DUO:0000026", "DUO:0000027",
            "DUO:0000028", "DUO:0000029", "DUO:0000042"
        ]
        self.ids_need_modifiers_with_def = {
            "DUO:0000024": "This DUO Term requires you specify date as YYYY-MM-DD format in the modifier attribute."
        }

    def validate_duo(self):
        validity = True
        duo_list = self.input_json.get('duo')

        # if duo_list is empty or None, abort validation right away
        if not duo_list:
            return False

        for duo in duo_list:

            duo_id = duo.get("id")
            modifier = duo.get("modifier")

            # Fail if the ID is None
            if duo_id is None:
                validity = False
                print("Please specify 'id' for all DUO terms.")

            # Fail if the ID supplied is unsupported
            if duo_id not in self.ids_supported:
                validity = False
                print(duo_id, "is not supported.")

            # Fail if the modifier is not supplied with IDs that require it
            if duo_id in self.ids_need_modifiers_with_def and modifier is None:
                validity = False
                print(duo_id, self.ids_need_modifiers_with_def[duo_id])

            # Fail if the datetime supplied with the IDs that require it is invalid
            if duo_id in self.ids_require_datetime_modifier:
                if self.validate_date_time(modifier) is False:
                    validity = False
                    print(duo_id, "has malformed datetime", modifier, "it should be YYYY-MM-DD")

            # Fail if modifier is supplied with IDs that do not require it
            if modifier is not None and duo_id not in self.ids_need_modifiers_with_def:
                validity = False
                print(duo_id, "cannot accept a modifier.")

        return validity

    def validate_date_time(self, date):
        # Return True only if the date is formatted as YYYY-MM-DD
        try:
            datetime.strptime(str(date), "%Y-%m-%d")
        except (ValueError, TypeError):
            return False

        return True

    def get_duo_list(self):

        duo_list = self.input_json['duo']
        return json.dumps(duo_list)


class OntObjectInitiator():
    """
    This class makes it easier to initiate pronto Ontology object.

    Usage:
    ont = OntObjectInitiator("https://raw.githubusercontent.com/EBISPOT/DUO/master/src/ontology/duo-basic.owl").get_ont()
    term = OntologyParser(ont, "DUO:0000024")
    """

    def __init__(self, url):
        self.ontology_link = url

    def get_ont(self):
        """
        Return an Ontology object that is ready to use.
        """
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")

            try:
                return Ontology(self.ontology_link)
            except ValueError:
                # Fail to parse
                raise exceptions.FailToParseOntologyException()
            except Exception:
                # from None suppresses all previous exceptions.
                raise exceptions.NoInternetConnectionException() from None