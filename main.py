'''
Test ReqRes API
'''

import unittest
import requests

class TestApi(unittest.TestCase):
    '''
    TestApi
    '''
    def setUp(self):
        self.__api = "https://reqres.in/api"
        self.__headers = {
            "Content-Type": "application/json", 
            "x-api-key": "reqres-free-v1"
        }
        self.__timeout = 10
        self.__user_id = 2

    def test_get_user(self):
        '''
        Test GET HTTP-request
        '''
        res = requests.get(
            f"{self.__api}/users/{self.__user_id}",
            headers=self.__headers,
            timeout=self.__timeout
        )

        assert res.status_code == 200, "The status code is not 200"

        result = res.json()
        assert "data" in result, "There is no data in the response"

        user = result["data"]
        required_fields = ["id", "email", "first_name", "last_name", "avatar"]
        for field in required_fields:
            assert field in user, f"The {field} field is missing"

        assert user["id"] == self.__user_id, "Invalid user ID"
        assert "@" in user["email"], "Incorrect email address"

    def test_add_user(self):
        '''
        Test POST HTTP-request
        '''
        body = {
            "name": "Kayuda Kirill",
            "job": "Developer"
        }

        res = requests.post(
            f"{self.__api}/users",
            json=body,
            headers=self.__headers,
            timeout=self.__timeout
        )

        assert res.status_code == 201, "The status code is not 201"

        result = res.json()

        expected_keys = [ "name", "job", "id", "createdAt" ]
        for key in expected_keys:
            assert key in result, f"Missing field: {key}"

        assert isinstance(result["id"], str), "ID should be string"

        assert result["name"] == body["name"], "Invalid name"
        assert result["job"] == body["job"], "Invalid job"

    def test_update_user(self):
        '''
        Test PUT HTTP-request
        '''
        body = {
            "name": "Kayuda Kirill",
            "job": "Lead"
        }

        res = requests.put(
            f"{self.__api}/users/2",
            json=body,
            headers=self.__headers,
            timeout=self.__timeout
        )

        assert res.status_code == 200, "The status code is not 200"

        result = res.json()

        expected_keys = [ "name", "job", "updatedAt" ]
        for key in expected_keys:
            assert key in result, f"Missing field: {key}"

        assert result["name"] == body["name"], "Invalid name"
        assert result["job"] == body["job"], "Invalid job"
