import copy
import datetime
import json

from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework.exceptions import ValidationError as DrfValidationError

from lunch_selector.test_utils import CustomAPITestCase
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

        yesterday = datetime.datetime.today().date() - datetime.timedelta(days=1)
        self.yesterday_menu = Menu(
            restaurant=restaurant,
            name="test menu",
            details="Corn Soup\nSalad with Chicken\nRoasted Vegetables",
            day=yesterday
        )
        self.yesterday_menu.save()

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

    def test_vote_yesterday_menu(self):
        serializer = MenuVoteSerializer(data={
            "menu": self.yesterday_menu.id,
            "employee": self.employee_instance.id
        })
        self.assertEqual(serializer.is_valid(), False)
        self.assertRaisesRegex(
            AssertionError, r"You cannot call .*? on a serializer with invalid data.",
            serializer.save
        )


class MenuVoteViewsTest(CustomAPITestCase):

    def setUp(self):
        super().setUp()
        self.url_vote = reverse("vote-list")
        restaurant1 = Restaurant(
            name="test restaurant 1",
            manager=self.manager_instance
        )
        restaurant1.save()
        restaurant2 = Restaurant(
            name="test restaurant 2",
            manager=self.manager_instance
        )
        restaurant2.save()

        self.menu1 = Menu(
            restaurant=restaurant1,
            name="test menu",
            details="Corn Soup\nSalad with Chicken\nRoasted Vegetables"
        )
        self.menu1.save()

        self.menu2 = Menu(
            restaurant=restaurant2,
            name="test menu",
            details="Corn Soup\nSalad with Chicken\nRoasted Vegetables"
        )
        self.menu2.save()

        yesterday = datetime.datetime.today().date() - datetime.timedelta(days=1)
        self.yesterday_menu = Menu(
            restaurant=restaurant1,
            name="test menu",
            details="Corn Soup\nSalad with Chicken\nRoasted Vegetables",
            day=yesterday
        )
        self.yesterday_menu.save()

        self.valid_data = {
            "menu": self.menu1.id
        }

    def test_vote_url_without_token(self):
        response = self.client.get(self.url_vote)
        self.assertEqual(response.status_code, 401)
        response = self.client.get(f"{self.url_vote}1/")
        self.assertEqual(response.status_code, 401)

    def test_non_permitted_users(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.manager_token.key}")
        response = self.client.get(self.url_vote)
        self.assertEqual(response.status_code, 403)
        self.assertRegex(
            json.dumps(response.data),
            "You do not have permission to perform this action"
        )

        response = self.client.get(f"{self.url_vote}1/")
        self.assertEqual(response.status_code, 403)

        response = self.client.post(self.url_vote, data=self.valid_data)
        self.assertEqual(response.status_code, 403)

        response = self.client.put(f"{self.url_vote}1/", data=self.valid_data)
        self.assertEqual(response.status_code, 403)

        response = self.client.get(f"{self.url_vote}result/", data=self.valid_data)
        self.assertEqual(response.status_code, 403)

    def test_vote_yesterday_menu(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.employee_token.key}")
        response = self.client.post(
            self.url_vote,
            data={"menu": self.yesterday_menu.id}
        )
        self.assertEqual(response.status_code, 400)
        self.assertRegex(
            json.dumps(response.data),
            "Menu is not from today"
        )

    def test_crud_vote(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.employee_token.key}")
        # Vote on menu
        response = self.client.post(self.url_vote, data=self.valid_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["menu"], self.valid_data["menu"])
        self.assertEqual(
            response.data["day"],
            datetime.datetime.today().strftime("%Y-%m-%d")
        )

        # Vote on same menu again
        response = self.client.post(self.url_vote, data=self.valid_data)
        self.assertEqual(response.status_code, 400)
        self.assertRegex(
            json.dumps(response.data),
            "The fields employee, day must make a unique set"
        )

        # Vote get
        response = self.client.get(self.url_vote)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["id"], 1)
        self.assertEqual(response.data[0]["menu"], self.valid_data["menu"])

        # Vote update
        response = self.client.put(
            f"{self.url_vote}{response.data[0]['id']}/",
            data={"menu": self.menu2.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["menu"], self.menu2.id)

        # result
        response = self.client.get(
            f"{self.url_vote}result/",
            data={"menu": self.menu2.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["name"], self.menu2.name)
        self.assertEqual(response.data[0]["details"], self.menu2.details)
