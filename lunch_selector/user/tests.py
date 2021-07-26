"""user app test cases"""
import copy
import json

from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework.exceptions import ValidationError

from lunch_selector.test_utils import CustomAPITestCase
from .models import SelectorUser
from .serializers import UserSerializer


class SelectorUserModelTest(TestCase):

    def test_valid_user(self):
        user = SelectorUser(username="test", user_type="employee")
        user.save()
        self.assertEqual(user.username, "test")
        self.assertEqual(user.user_type, SelectorUser.EMPLOYEE)

    def test_unique_username(self):
        user = SelectorUser(username="test", user_type="employee")
        user.save()
        user2 = SelectorUser(username="test", user_type="employee")
        self.assertRaisesRegex(
            IntegrityError, "UNIQUE constraint failed: user_selectoruser.username",
            user2.save
        )


class UserSerializerTest(TestCase):

    def test_required_fields(self):
        fields = ["username", "password", "confirm_password", "user_type"]
        valid_data = {
            "username": "test_user",
            "password": "h@rd-p@$$w0rd",
            "confirm_password": "h@rd-p@$$w0rd",
            "user_type": "admin"
        }
        for field in fields:
            _data = copy.deepcopy(valid_data)
            _data.pop(field)
            serializer = UserSerializer(data=_data)
            self.assertEqual(serializer.is_valid(), False)
            self.assertRaisesRegex(
                ValidationError, f"{field}.*?This field is required",
                serializer.is_valid, raise_exception=True
            )

    def test_invalid_password(self):
        invalid_passwords = {
            "test": ["This password is too short", "This password is too common"],
            "1234": ["This password is too short", "This password is too common"],
            "hello": ["This password is too short", "This password is too common"],
            "helloworld": ["This password is too common"],
            "": ["This field may not be blank."]
        }

        for password, errors in invalid_passwords.items():
            serializer = UserSerializer(
                data={"username": "test_user", "password": password, "confirm_password": password}
            )
            self.assertEqual(serializer.is_valid(), False)

            for error in errors:
                self.assertRaisesRegex(
                    ValidationError, error,
                    serializer.is_valid, raise_exception=True
                )

    def test_match_password(self):
        serializer = UserSerializer(
            data={
                "username": "test_user",
                "password": "th1s-1s-h@rd-p@$$w0rd",
                "confirm_password": "not-following-password",
                "user_type": "admin"
            }
        )
        self.assertEqual(serializer.is_valid(), False)
        self.assertRaisesRegex(
            ValidationError, "password should be equal to confirm_password",
            serializer.is_valid, raise_exception=True
        )

    def test_create_user(self):
        serializer = UserSerializer(
            data={
                "username": "test_user",
                "password": "h@rd-p@$$w0rd",
                "confirm_password": "h@rd-p@$$w0rd",
                "user_type": "employee"
            }
        )
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()


class UserViewsTest(CustomAPITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse("user-create")
        cls.valid_data = {
            "username": "test-user",
            "password": "h@rd-p@$$w0rd",
            "confirm_password": "h@rd-p@$$w0rd",
            "user_type": "employee"
        }

    def test_user_create_without_token(self):
        resp = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(resp.status_code, 401)
        self.assertRegex(json.dumps(resp.data), "Authentication credentials were not provided.")

    def test_create_user_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.manager_token.key}")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 403)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.employee_token.key}")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 403)

    def test_create_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["username"], self.valid_data["username"])
        self.assertEqual(response.data["user_type"], self.valid_data["user_type"])

    def test_user_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        url = reverse("logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)
