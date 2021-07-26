"""user app test cases"""
import copy

from django.db import IntegrityError
from django.test import TestCase
from rest_framework.exceptions import ValidationError

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
