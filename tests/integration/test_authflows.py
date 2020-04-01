"""
Set of tests used to connect an integrated, bootstrapped
API Gateway + Keycloak + Data Server deployment

NOTE: Pre-configuration required. Tyk and Keycloak must be configured to communicate with the data server
"""

import requests
import unittest
import json
import time
import logging

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    WebDriverException,
)


logger = logging.getLogger(__file__)

with open('tests/integration/config.json', 'r') as test_config:
    parsed_config = json.load(test_config)
    TEST_USER = parsed_config['username']
    TEST_PW = parsed_config['password']
    TYK_HOST = parsed_config['tyk']


class TestIntegrationApi(unittest.TestCase):

    def openLeftSidebarMenu(self, driver, classname):
        """
        This method receives the driver itself and a HTML class name as args.
        The purpose of this method is to open the side bar menu
        when the page is on its "mobile" version.
        """
        try:
            # If "classname" is "clickable" it will expand side bar menu
            driver.find_elements_by_class_name(classname)[0].click()
            time.sleep(1.0)  # it needs time to expand the sidebar
        except ElementNotInteractableException:
            # Otherwise the excepetion is captured here and the method
            # does not do anything
            pass
        except IndexError:
            pass

    def openRightSideMenu(self, driver, target):
        """
        This method receives the driver itself and a data target tag value
        (such as data-target="#navigation") as args.
        The purpose of this method is to open the side bar menu
        when the page is on its "mobile" version.
        """
        try:
            # If "target" is "clickable" it will expand side bar menu
            driver.find_elements_by_xpath(target)[0].click()
            time.sleep(1.0)  # it needs time to expand the sidebar
        except ElementNotInteractableException:
            # Otherwise the excepetion is captured here and the method
            # does not do anything
            pass

    def api_login(self, username, password):
        # auth requests must be sent through gateway server
        token_endpoint = '{}/auth/token'.format(TYK_HOST)
        headers = {'Content-type': 'application/json'}
        body = {'username': username, 'password': password}
        r = requests.post(token_endpoint, data=json.dumps(body), headers=headers)
        r_json = r.json()
        self.assertIsNot(type(r_json), str)
        return {"code": r.status_code, "body": r_json}

    def browser_login(self, driver):
        try:
            driver.get(TYK_HOST)
        except (ConnectionError, WebDriverException):
            driver.quit()
            self.assertTrue(False, msg="Could not load driver")

        try:
            username_dom = driver.find_element_by_id("username")
            password_dom = driver.find_element_by_id("password")
            
            username_dom.send_keys([TEST_USER])
            password_dom.send_keys([TEST_PW])

            driver.find_element_by_id("kc-login").click()
            time.sleep(2.0)

            self.openLeftSidebarMenu(driver, "navbar-toggler")

            driver.find_element_by_link_text("GENE SEARCH").click()
            time.sleep(1.5)

            # Everytime the code perform a "click" on a menu item
            # the menu "shrink" so we need to expand it again
            self.openLeftSidebarMenu(driver, "navbar-toggler")

            driver.find_element_by_link_text("PATIENT OVERVIEW").click()
            time.sleep(1.5)

            self.openLeftSidebarMenu(driver, "navbar-toggler")

            driver.find_element_by_link_text("SAMPLE ANALYSIS").click()
            time.sleep(1.5)
            driver.find_element_by_id("sampleSearch").click()
            time.sleep(1.5)

            self.openLeftSidebarMenu(driver, "navbar-toggler")
            
            driver.find_element_by_link_text("CUSTOM VISUALIZATION").click()
            time.sleep(1.5)
            driver.find_element_by_id("adv1_confirm").click()
            time.sleep(1.5)
            driver.find_element_by_id("adv2_confirm").click()
            time.sleep(1.5)

            self.openRightSideMenu(driver, "//*[@data-target='#navigation']")            
            
            driver.find_element_by_id("user-dropdown-top").click()
            time.sleep(1.0)
            driver.find_element_by_link_text("Logout").click()
            driver.quit()

        except NoSuchElementException:
            driver.quit()
            self.assertTrue(False, msg="Could not complete login/logout flow")

    def testFirefoxAuthFlow(self):
        """
        Performs a Firefox browser login and logout
        """
        options = FireFoxOptions()
        options.headless = True
        driver = webdriver.Firefox(options=options)  # requires geckodriver defined in $PATH
        self.browser_login(driver)

    def testChromeAuthFlow(self):
        """
        Performs a Chrome browser login and logout
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)  # requires chromedriver defined in $PATH

        self.browser_login(driver)

    def testInvalidCredentials(self):
        login_response = self.api_login('invalid_user', 'invalid_password')
        self.assertIn(login_response["code"], [401, 403])
        token = login_response["body"].get("id_token")
        self.assertIsNone(token)

    def testTokenAuthFlow(self):
        """
        Ensure that the testing KC server has a test user loaded into it
        """
        login_response = self.api_login(TEST_USER, TEST_PW)
        self.assertEqual(login_response["code"], 200)
        token = login_response["body"].get("id_token")
        logger.info('got token {}'.format(token))
        logger.debug('got token {}'.format(login_response))

        token_as_bearer = 'Bearer {}'.format(token)
        headers = {'Authorization': token_as_bearer}
        test_endpoint = '{}/datasets/search'.format(TYK_HOST)

        r = requests.post(test_endpoint, data=json.dumps({}))
        logger.info('below is first test response')
        logger.debug(r.text)
        self.assertIn(r.status_code, [401, 403])

        r = requests.post(test_endpoint, data=json.dumps({}), headers=headers)
        logger.info('below is second test response')
        logger.debug(r.text)
        self.assertEqual(r.status_code, 200)
