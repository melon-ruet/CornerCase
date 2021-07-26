import copy
import datetime

from django.db import IntegrityError
from django.test import TestCase
from rest_framework.exceptions import ValidationError as DrfValidationError

from restaurant.models import Restaurant, Menu
from vote.models import MenuVote
from user.models import SelectorUser
from vote.serializers import MenuVoteSerializer


class MenuVoteSetup(TestCase):

    def setUp(self):
        manager_instance = SelectorUser(
            username="manager",
            user_type=SelectorUser.RESTAURANT_MANAGER
        )
        manager_instance.save()

        self.employee_instance = SelectorUser(
            username="employee",
            user_type=SelectorUser.EMPLOYEE
        )
        self.employee_instance.save()

        restaurant = Restaurant(name="restaurant", manager=manager_instance)
        restaurant.save()
        self.menu = Menu(
            restaurant=restaurant,
            name="test menu",
            details="Corn Soup\nSalad with Chicken\nRoasted Vegetables"
        )
        self.menu.save()

        self.valid_menu_vote_data = {
            "menu": self.menu.id,
            "employee": self.employee_instance.id
        }


class MenuVoteModelTest(MenuVoteSetup):

    def test_valid_vote(self):
        vote = MenuVote(menu=self.menu, employee=self.employee_instance)
        vote.save()
        self.assertEqual(vote.menu, self.menu)
        self.assertEqual(vote.employee, self.employee_instance)
        self.assertEqual(vote.day, datetime.datetime.today().date())
        self.assertEqual(vote.menu.vote_count, 1)

    def test_multi_vote_same_menu(self):
        vote = MenuVote(menu=self.menu, employee=self.employee_instance)
        vote.save()

        vote2 = MenuVote(menu=self.menu, employee=self.employee_instance)
        self.assertRaisesRegex(
            IntegrityError, "UNIQUE constraint failed: vote_menuvote.employee_id, vote_menuvote.day",
            vote2.save
        )


class MenuVoteSerializerTest(MenuVoteSetup):

    def test_required_fields(self):
        fields = ["menu", "employee"]
        for field in fields:
            _data = copy.deepcopy(self.valid_menu_vote_data)
            _data.pop(field)
            serializer = MenuVoteSerializer(data=_data)
            self.assertEqual(serializer.is_valid(), False)
            self.assertRaisesRegex(
                DrfValidationError, f"{field}.*?This field is required",
                serializer.is_valid, raise_exception=True
            )

    def test_create_menu_vote(self):
        serializer = MenuVoteSerializer(data=self.valid_menu_vote_data)
        self.assertEqual(serializer.is_valid(raise_exception=True), True)
        vote = serializer.save()
        self.assertIsInstance(vote, MenuVote)

    def test_vote_more_than_once_same_menu(self):
        serializer = MenuVoteSerializer(data=self.valid_menu_vote_data)
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        serializer = MenuVoteSerializer(data=self.valid_menu_vote_data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertRaisesRegex(
            AssertionError, r"You cannot call .*? on a serializer with invalid data.",
            serializer.save
        )
