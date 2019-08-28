"""
Methods and helpers for creating a Federated Response object
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import base64
import requests
import flask

import candig.schemas.protocol as protocol
import candig.server.exceptions as exceptions

from collections import Counter
from requests_futures.sessions import FuturesSession


class FederationResponse(object):
    """
    Federate the queries by iterating through the peer list and merging the
    result.

    Parameters:
    ===========
    endpoint: method
        Method of a datamodel object that populates the response
    request: string
        Request send along with the query, like: id for GET requests
    response_format: protocol.Message
        Response class to use when forming results object from serialized protobuf
    return_mimetype: string
        'http/json or application/json'
    request_type: string
        Specify whether the request is a "GET" or a "POST" request
    request_dict: dict
        flask request dictionary
    app:
        the flask application context
    """
    def __init__(self, request, endpoint, response_format, request_type, return_mimetype, request_dict, app):
        self.proto = None
        self.app = flask.current_app
        self.results = {}
        self.response_format = response_format
        self.status = []
        self.request = request
        self.endpoint = endpoint
        self.request_type = request_type
        self.return_mimetype = return_mimetype
        self.request_dict = request_dict
        self.token, self.access_map = self.handle_access_permissions()

    def handle_access_permissions(self):
        """
        user roles are loaded in to the server from the access_list.txt
        a user-specific access map is generated here based on the id_token and
        the in-memory server side access map

        if running NoAuth config, user has full access to local datasets

        :return: jwt token, python dict in the form {"project" : "access tier", ...}
        """

        access_map = {}

        if self.app.config.get("TYK_ENABLED"):
            if 'Authorization' in self.request_dict.headers:
                access_token = self.request_dict.headers['Authorization']
                parsed_payload = get_jwt_payload(access_token)
                issuer = parsed_payload.get('iss')
                username = parsed_payload.get('preferred_username')
                access_map = self.app.access_map.getUserAccessMap(issuer, username)
            else:
                raise exceptions.NotAuthenticatedException
        else:
            # for dev: mock full access when not using TYK config
            access_token = None
            for dataset in self.app.serverStatus.getDatasets():
                access_map[dataset.getLocalId()] = 4

        return access_token, access_map

    def handle_local_request(self):
        """
        make local data request and set the results and status for a FederationResponse
        """
        try:
            self.proto = self.endpoint(
                self.request,
                return_mimetype="application/octet-stream",
                access_map=self.access_map
            )

            self.status.append(200)

        except (exceptions.ObjectWithIdNotFoundException, exceptions.NotFoundException):
            self.status.append(404)

        except (exceptions.NotAuthorizedException):
            self.status.append(401)

        print(">>> Local Response: " + str(self.status[0]))

    def handle_peer_request(self, request_type):
        """
        make peer data requests and update the results and status for a FederationResponse
        """

        header = {
            'Content-Type': self.return_mimetype,
            'Accept': 'application/octet-stream',
            'Federation': 'False',
            'Authorization': self.token,
        }

        uri_list = []
        for peer in self.app.serverStatus.getPeers():
            uri = self.request_dict.url.replace(
                self.request_dict.host_url,
                peer.getUrl(),
            )
            uri_list.append(uri)

        for future_response in self.async_requests(uri_list, request_type, header):
            try:
                response = future_response.result()
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                self.status.append(503)
                continue
            self.status.append(response.status_code)
            # If the call was successful, merge protocol buffers
            if response.status_code == 200:
                peer_response = response.content
                peer_msg = self.response_format()
                peer_msg.ParseFromString(peer_response)
                self.proto.MergeFrom(peer_msg)

        if self.endpoint == self.app.backend.runCountQuery and self.results:
            self.merge_counts()

    def merge_counts(self):
        """
        merge federated counts and set results for a FederationResponse
        """
        table = list(set(self.results.keys()) - {"nextPageToken", "total"})[0]
        prepare_counts = {}
        for record in self.results[table]:
            for k, v in record.items():
                if k in prepare_counts:
                    prepare_counts[k].append(Counter(v))
                else:
                    prepare_counts[k] = [Counter(v)]

        merged_counts = {}
        for field in prepare_counts:
            count_total = Counter()
            for count in prepare_counts[field]:
                count_total = count_total + count
            merged_counts[field] = dict(count_total)
        self.results[table] = [merged_counts]

    def get_response_object(self):
        """
        Returns:
        ========
        responseObject: json string
            Merged responses from the servers. responseObject structure:

        {
        "status": {
            "Successful communications": <number>,
            "Known peers": <number>,
            "Valid response": <true|false>,
            "Queried peers": <number>
            },
        "results": {
                "total": N
                "datasets": [
                        {record1},
                        {record2},
                        ...
                        {recordN},
                    ]
                }
            ]
        }
        """
        if self.proto:
            if isinstance(self.proto, str):
                s = self.proto
            else:
                s = protocol.serialize(self.proto, self.return_mimetype)
            self.results = json.loads(s)
        responseObject = {'status': self.status, 'results': self.results}
        # If no result has been found on any of the servers raise an error
        if not responseObject['results']:
            if self.request_type == 'GET':
                raise exceptions.ObjectWithIdNotFoundException(self.request)
            elif self.request_type == 'POST':
                raise exceptions.ObjectWithIdNotFoundException(json.loads(self.request))
        else:
            # Update total
            table = list(set(responseObject['results'].keys()) - {"nextPageToken", "total"})[0]
            if self.endpoint != self.app.backend.runCountQuery:
                responseObject['results']['total'] = len(responseObject['results'][table])

        # Reformat the status response
        responseObject['status'] = {

            # All the peers plus self
            'Known peers': len(self.app.serverStatus.getPeers()) + 1,

            # Queried means http status code 200 and 404
            'Queried peers': responseObject['status'].count(200) + responseObject['status'].count(404),

            # Successful means http status code 200
            'Successful communications': responseObject['status'].count(200),

            # Invalid by default
            'Valid response': False
        }

        # Decide on valid response
        if responseObject['status']['Known peers'] == \
                responseObject['status']['Queried peers']:
            if self.request_type == 'GET':
                if responseObject['status']['Successful communications'] >= 1:
                    responseObject['status']['Valid response'] = True
            elif self.request_type == 'POST':
                if responseObject['status']['Successful communications'] == \
                        responseObject['status']['Queried peers']:
                    responseObject['status']['Valid response'] = True

        return responseObject

    def async_requests(self, uri_list, request_type, header):
        """
        Use futures session type to async process peer requests
        :return: list of future responses
        """
        async_session = FuturesSession(max_workers=10)  # capping max threads
        if request_type == "GET":
            responses = [
                async_session.get(uri, headers=header)
                for uri in uri_list
            ]
        elif request_type == "POST":
            responses = [
                async_session.post(uri, json=json.loads(self.request), headers=header)
                for uri in uri_list
            ]
        else:
            responses = []
        return responses

    def is_federated(self):
        # Check headers for federation. Federate by default
        return 'Federation' not in self.request_dict.headers or \
               self.request_dict.headers.get('Federation') == 'True'

    def get_proto(self):
        """
        :return: proto buf object
        """
        return self.proto


def get_jwt_payload(token):
    try:
        token_payload = token.split(".")[1]

        # make sure token is padded properly for b64 decoding
        padding = len(token_payload) % 4
        if padding != 0:
            token_payload += '=' * (4 - padding)
        decoded_payload = base64.b64decode(token_payload)

    except IndexError:
        decoded_payload = '{}'
    return json.loads(decoded_payload)
