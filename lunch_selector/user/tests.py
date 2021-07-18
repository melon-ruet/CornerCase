"""user app test cases"""
from django.test import TestCase

from .models import SelectorUser


class SelectorUserModelTest(TestCase):

    def test_user_type(self):
        user = SelectorUser(
            user_type=SelectorUser.ADMIN
        )
        self.assertEqual(user.user_type, user.ADMIN)
