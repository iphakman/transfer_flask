# -*- coding: utf-8 -*-
import json
import unittest

from flask import url_for

from app import create_app, db
from app.models import User


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.app_context.pop()

    def get_api_headers(self):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def test_create_user_success(self):
        params = {"msisdn": "254717416435", "first_name": "TestName", "last_name": "TestSurname"}
        url = url_for("api.users_post")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        saved_user = User.query.filter(User.msisdn == "254717416435").first()

        self.assertEqual(201, response.status_code)
        self.assertTrue(saved_user.msisdn == "254717416435")

    def test_create_user_missing_first_name(self):
        params = {"msisdn": "254717416435", "last_name": "TestSurname"}
        url = url_for("api.users_post")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        json_response = json.loads(response.data.decode("utf-8"))

        self.assertEqual(400, response.status_code)
        self.assertTrue("error" in json_response)
        error = json_response["error"]
        self.assertEqual(400, response.status_code)
        self.assertEquals(["First name is required."], error)

    def test_create_user_missing_last_name(self):
        params = {"msisdn": "254717416435", "first_name": "TestName"}
        url = url_for("api.users_post")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        json_response = json.loads(response.data.decode("utf-8"))

        self.assertEqual(400, response.status_code)
        self.assertTrue("error" in json_response)
        error = json_response["error"]
        self.assertEqual(400, response.status_code)
        self.assertEquals(["Last name is required."], error)

    def test_create_user_missing_msisdn(self):
        params = {"first_name": "TestName", "last_name": "TestSurname"}
        url = url_for("api.users_post")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        json_response = json.loads(response.data.decode("utf-8"))

        self.assertEqual(400, response.status_code)
        self.assertTrue("error" in json_response)
        error = json_response["error"]
        self.assertEqual(400, response.status_code)
        self.assertEquals(["Phone number is required."], error)

    def test_create_user_invalid_msisdn(self):
        params = {"msisdn": "abd254717416435", "first_name": "TestName", "last_name": "TestSurname"}
        url = url_for("api.users_post")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        json_response = json.loads(response.data.decode("utf-8"))

        self.assertEqual(400, response.status_code)
        self.assertTrue("error" in json_response)
        error = json_response["error"]
        self.assertEqual(400, response.status_code)
        self.assertEquals(["Phone number must contain just numbers."], error)

    def test_create_user_error_user_already_exists(self):
        user = User(msisdn="254717416435")
        db.session.add(user)
        db.session.commit()

        params = {"msisdn": "254717416435", "first_name": "TestName", "last_name": "TestSurname"}
        url = url_for("api.users_post")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        json_response = json.loads(response.data.decode("utf-8"))

        self.assertEqual(400, response.status_code)
        self.assertTrue("error" in json_response)
        error = json_response["error"]
        self.assertEqual(400, response.status_code)
        self.assertEquals(["User with that phone number already exists."], error)
