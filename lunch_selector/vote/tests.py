import datetime

from django.db import IntegrityError
from django.test import TestCase

from restaurant.models import Restaurant, Menu
from vote.models import MenuVote
from user.models import SelectorUser


class VoteModelTest(TestCase):

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
