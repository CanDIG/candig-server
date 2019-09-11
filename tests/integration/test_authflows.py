"""
Set of tests used to connect an integrated, bootstrapped
API Gateway + Keycloak + Data Server deployment

NOTE: Pre-configuration required. Tyk and Keycloak must be configured to communicate with the data server
"""

import requests
import unittest
import json
import csv

import tests.paths as paths

with open('tests/integration/config.json', 'r') as test_config:
    parsed_config = json.load(test_config)
    TEST_USER = parsed_config['username']
    TEST_PW = parsed_config['password']
    TYK_HOST = parsed_config['tyk']
    KC_HOST = parsed_config['keycloak']
    KC_REALM = parsed_config['realm']
    KC_CLIENT = parsed_config['client']


@unittest.skip("Enable this when continuous test deployment of Tyk/KC works")
class TestIntegrationApi(unittest.TestCase):
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
        callback = TYK_HOST + '/login_oidc'
        redirect_url = '{0}/auth/realms/{1}/protocol/openid-connect/auth?scope=openid+email&response_type=code&' \
                       'client_id={2}&response_mode=form_post&redirect_uri={3}&return_url={4}/'.format(
                        KC_HOST, KC_REALM, KC_CLIENT, callback, TYK_HOST
        )
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
        # self.build_acl(KC_HOST, KC_REALM, TEST_USER)
        r = requests.post(test_endpoint, data=json.dumps({}), headers=headers)
        self.assertEqual(r.status_code, 200)

        # # acl should be empty resulting in 404
        # self.clear_acl()
        # r = requests.post(test_endpoint, data=json.dumps({}), headers=headers)
        # self.assertEqual(r.status_code, 404)
