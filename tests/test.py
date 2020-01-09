import os
import sys
import unittest

import numpy as np
import requests

# sys.path.append("../")

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)
from myapp import app


def authenticate():
    # first authenticate
    url = "http://127.0.0.1:3000/auth"

    payload = '{\n\t"username": "bruno",\n\t"password": "asdf"\n}\n'
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    # token = response.text.decode("utf8")
    token = response.json()["access_token"]
    return response.status_code, token


class ProjectTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        self.app = app.test_client()

        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        super(ProjectTests, self).tearDown()

    ########################
    #### helper methods ####
    ########################

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get("/", follow_redirects=True)

        assert response.status_code == 200
        assert response.data == b"Hello, world!"

    def test_register(self):

        url = "http://127.0.0.1:3000/register"

        payload = '{\n\t"username": "bruno",\n\t"password": "asdf"\n}\n'
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.json()["message"])
        assert response.status_code == 400  # user already exists

    # #
    # # #
    #
    def test_auth(self):
        status, dummy = authenticate()

        assert status == 200

    # #
    # # #
    def test_post_resource_already_exists(self):
        status, token = authenticate()
        url = "http://127.0.0.1:3000/item/test"

        payload = '{\n\t"price": 10.99\n}'
        headers = {
            "Content-Type": "application/json",
            "Authorization": "JWT  " + str(token),
        }

        response = requests.request("POST", url, headers=headers, data=payload)

    #     assert response.status_code == 400

    #
    def test_post_resource_doesnot_exist(self):
        status, token = authenticate()

        url = "http://127.0.0.1:3000/item/desk" + str(
            np.random.randint(low=0, high=100, size=1)
        )

        payload = '{\n\t"price": 10.99\n}'
        headers = {
            "Content-Type": "application/json",
            "Authorization": "JWT  " + str(token),
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        assert response.status_code == 201

    def test_put_resource_doesnot_exist(self):
        status, token = authenticate()
        url = "http://127.0.0.1:3000/item/test" + str(
            np.random.randint(low=0, high=100, size=1)
        )

        payload = '{\n\t"price": 10.99\n}'
        headers = {
            "Content-Type": "application/json",
            "Authorization": "JWT " + str(token),
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        assert response.status_code == 201

    def test_put_resource_exists(self):
        status, token = authenticate()
        url = "http://127.0.0.1:3000/item/desk" + str(
            np.random.randint(low=0, high=100, size=1)
        )

        payload = '{\n\t"price": 212.99\n}'
        headers = {
            "Content-Type": "application/json",
            "Authorization": "JWT " + str(token),
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        assert response.status_code == 201

    def test_delete(self):
        status, token = authenticate()

        url = "http://127.0.0.1:3000/item/test"

        payload = {}
        headers = {
            "Authorization": "JWT " + str(token),
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)

        # print(response.json()["message"])
        assert response.json()["message"] == "item deleted"

    def test_items(self):
        status, token = authenticate()

        url = "http://127.0.0.1:3000/items"

        payload = {}
        headers = {
            "Authorization": "JWT " + str(token),
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text.encode("utf8"))


if __name__ == "__main__":
    import xmlrunner

    runner = xmlrunner.XMLTestRunner(output="tests/test-reports")
    unittest.main(testRunner=runner)
    ###########################################
    unittest.main()
