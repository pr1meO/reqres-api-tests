'''
Test ReqRes API
'''

import requests

class TestApi():
    '''
    TestApi
    '''
    def setup_method(self):
        '''
        Set Up
        '''
        self.api = "https://reqres.in/api"
        self.headers = {
            "Content-Type": "application/json", 
            "x-api-key": "reqres-free-v1"
        }
        self.timeout = 10
        self.user_id = 2

    def test_get_user(self):
        '''
        Test GET HTTP-request
        '''
        res = requests.get(
            f"{self.api}/users/{self.user_id}",
            headers=self.headers,
            timeout=self.timeout
        )

        assert res.status_code == 200, "The status code is not 200"

        result = res.json()
        assert "data" in result, "There is no data in the response"

        user = result["data"]
        required_fields = ["id", "email", "first_name", "last_name", "avatar"]
        for field in required_fields:
            assert field in user, f"The {field} field is missing"

        assert user["id"] == self.user_id, "Invalid user ID"
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
            f"{self.api}/users",
            json=body,
            headers=self.headers,
            timeout=self.timeout
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
            f"{self.api}/users/2",
            json=body,
            headers=self.headers,
            timeout=self.timeout
        )

        assert res.status_code == 200, "The status code is not 200"

        result = res.json()

        expected_keys = [ "name", "job", "updatedAt" ]
        for key in expected_keys:
            assert key in result, f"Missing field: {key}"

        assert result["name"] == body["name"], "Invalid name"
        assert result["job"] == body["job"], "Invalid job"
