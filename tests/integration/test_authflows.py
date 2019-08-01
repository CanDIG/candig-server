"""
Set of tests used to connect an integrated, bootstrapped
API Gateway + Keycloak + Data Server deployment

NOTE: Pre-configuration required. Tyk and Keycloak must be configured to communicate with the data server
"""

import requests
import unittest
import json
import csv

from tests.end_to_end import server_test
from tests.end_to_end import server

import candig.server.frontend as frontend
import tests.paths as paths

with open('tests/integration/config.json', 'r') as test_config:
    parsed_config = json.load(test_config)
    TEST_USER = parsed_config['username']
    TEST_PW = parsed_config['password']
    TYK_HOST = parsed_config['tyk']
    KC_HOST = parsed_config['keycloak']
    KC_REALM = parsed_config['realm']
    KC_CLIENT = parsed_config['client']

# SKIP_FLAG = 0 when continuous test deployment if Tyk/KC works
SKIP_FLAG = 1


@unittest.skip("Enable this when continuous test deployment of Tyk/KC works")
class TestIntegrationStart(unittest.TestCase):
    def testIntegratedStart(self):
        app = server.CandigIntegrationTestServer(
            TYK_HOST, KC_HOST, KC_REALM, KC_CLIENT, paths.testDataRepo, paths.testAccessList)
        try:
            app.start()
        finally:
            app.shutdown()


@unittest.skip("Enable this when continuous test deployment of Tyk/KC works")
class TestIntegrationApi(server_test.ServerTestClass):
    @classmethod
    def setUpClass(cls):
        cls.otherSetup()
        cls.server = cls.getServer()
        if not SKIP_FLAG == 1:
            cls.server.start()

    @classmethod
    def getServer(cls):
        return server.CandigIntegrationTestServer(
            TYK_HOST, KC_HOST, KC_REALM, KC_CLIENT, paths.testDataRepo, paths.testAccessList)

    def login(self, username, password):
        # auth requests must be sent through gateway server
        token_endpoint = '{}/token'.format(TYK_HOST)
        headers = {'Content-type': 'application/json'}
        body = {'username': username, 'password': password}
        r = requests.post(token_endpoint, data=json.dumps(body), headers=headers)
        if r.status_code == 200:
            r_json = r.json()
            return r_json.get('token')
        else:
            return None

    def build_acl(self, kc_host, kc_realm, test_user):
        issuer = "{}/auth/realms/{}".format(kc_host, kc_realm)
        access_list = paths.testAccessList
        with open(access_list, 'w+') as acl:
            tsv_writer = csv.writer(acl, delimiter='\t', lineterminator='\n')
            tsv_writer.writerow(["issuer", "username", "dataset1"])
            tsv_writer.writerow([issuer, test_user, 4])

    def clear_acl(self):
        access_list = paths.testAccessList
        acl = open(access_list, 'w+')
        acl.close()

    def testDashboardRedirect(self):
        # Dashboard should be returning 302 to Keycloak login without token
        frontend.configure(baseConfig="KeycloakOidConfig", configFile=self.server.configFile.name)
        redirect_url = frontend._generate_login_url(TYK_HOST) + '/'
        r = requests.get(TYK_HOST, allow_redirects=False)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.headers['Location'], redirect_url)

    def testInvalidCredentials(self):
        token = self.login('invalid_user', 'invalid_password')
        self.assertIsNone(token)

    def testValidAuthFlow(self):
        """
        Ensure that the testing KC server has a test user loaded into it
        """
        token = self.login(TEST_USER, TEST_PW)
        self.assertIsNotNone(token)
        token_as_bearer = 'Bearer {}'.format(token)
        headers = {'Authorization': token_as_bearer}
        test_endpoint = '{}/datasets/search'.format(TYK_HOST)

        # no headers, should return 403
        r = requests.post(test_endpoint, data=json.dumps({}))
        self.assertEqual(r.status_code, 403)

        # after building the acl, should be 200
        self.build_acl(KC_HOST, KC_REALM, TEST_USER)
        r = requests.post(test_endpoint, data=json.dumps({}), headers=headers)
        self.assertEqual(r.status_code, 200)

        # acl should be empty resulting in 404
        self.clear_acl()
        r = requests.post(test_endpoint, data=json.dumps({}), headers=headers)
        self.assertEqual(r.status_code, 404)
