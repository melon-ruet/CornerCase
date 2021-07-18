from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from restaurant.models import Restaurant
from user.models import SelectorUser


class RestaurantModelTest(TestCase):

    def setUp(self):
        self.manager_instance = SelectorUser(
            username="manager",
            user_type=SelectorUser.RESTAURANT_MANAGER
        )
        self.manager_instance.save()

        self.employee_instance = SelectorUser(
            username="employee",
            user_type=SelectorUser.EMPLOYEE
        )
        self.employee_instance.save()

    def test_valid_restaurant(self):
        restaurant = Restaurant(name="test", manager=self.manager_instance)
        restaurant.save()
        self.assertEqual(restaurant.name, "test")
        self.assertEqual(restaurant.manager.id, self.manager_instance.id)

    def test_unique_restaurant_name(self):
        restaurant = Restaurant(name="test", manager=self.manager_instance)
        restaurant.save()

        restaurant2 = Restaurant(name="test", manager=self.manager_instance)
        self.assertRaises(IntegrityError, restaurant2.save)

    def test_non_manager_user(self):
        restaurant = Restaurant(name="test", manager=self.employee_instance)
        self.assertRaisesRegex(
            ValidationError, "user_type must be restaurant manager",
            restaurant.save
        )
