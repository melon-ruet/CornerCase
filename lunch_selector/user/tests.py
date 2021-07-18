"""user app test cases"""
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from .models import SelectorUser
from .serializers import UserSerializer


class SelectorUserModelTest(TestCase):

    def test_user_type(self):
        user = SelectorUser(
            user_type=SelectorUser.ADMIN
        )
        self.assertEqual(user.user_type, user.ADMIN)


class UserSerializerTest(TestCase):

    def test_without_password(self):
        serializer = UserSerializer(data={"username": "test_user"})
        self.assertEqual(serializer.is_valid(), False)
        self.assertRaises(ValidationError, serializer.is_valid, raise_exception=True)

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
                "confirm_password": "not-following-password"
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
                "confirm_password": "h@rd-p@$$w0rd"
            }
        )
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()
