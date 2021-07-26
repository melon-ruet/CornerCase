import copy
import datetime

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from rest_framework.exceptions import ValidationError as DrfValidationError

from restaurant.models import Restaurant, Menu
from restaurant.serializers import RestaurantSerializer, MenuSerializer
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


class RestaurantSerializerTest(TestCase):

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

    def test_required_fields(self):
        fields = ["name", "manager"]
        valid_data = {
            "name": "test_restaurant",
            "manager": self.manager_instance.id
        }
        for field in fields:
            _data = copy.deepcopy(valid_data)
            _data.pop(field)
            serializer = RestaurantSerializer(data=_data)
            self.assertEqual(serializer.is_valid(), False)
            self.assertRaisesRegex(
                DrfValidationError, f"{field}.*?This field is required",
                serializer.is_valid, raise_exception=True
            )

    def test_without_restaurant_manager(self):
        serializer = RestaurantSerializer(
            data={
                "name": "test_restaurant",
                "manager": self.employee_instance.id
            }
        )
        self.assertEqual(serializer.is_valid(), True)
        self.assertRaises(ValidationError, serializer.save)

    def test_create_restaurant(self):
        serializer = RestaurantSerializer(
            data={
                "name": "test_restaurant",
                "manager": self.manager_instance.id
            }
        )
        self.assertEqual(serializer.is_valid(), True)
        restaurant = serializer.save()
        self.assertIsInstance(restaurant, Restaurant)


class MenuModelTest(TestCase):

    def setUp(self):
        manager_instance = SelectorUser(
            username="manager",
            user_type=SelectorUser.RESTAURANT_MANAGER
        )
        manager_instance.save()
        self.restaurant1 = Restaurant(name="restaurant1", manager=manager_instance)
        self.restaurant1.save()
        self.restaurant2 = Restaurant(name="restaurant2", manager=manager_instance)
        self.restaurant2.save()
        self.restaurant3 = Restaurant(name="restaurant3", manager=manager_instance)
        self.restaurant3.save()

    def test_valid_menu(self):
        menu = Menu(
            restaurant=self.restaurant1,
            name="test menu",
            details="Corn Soup\nSalad with Chicken\nRoasted Vegetables"
        )
        menu.save()
        self.assertEqual(menu.name, "test menu")
        self.assertEqual(menu.restaurant.id, self.restaurant1.id)
        self.assertEqual(menu.day, datetime.date.today())
        self.assertEqual(menu.vote_count, 0)

    def test_unique_restaurant_day_menu(self):
        menu1 = Menu(
            restaurant=self.restaurant1,
            name="test menu 1",
            details="Corn Soup\nSalad with Chicken\nRoasted Vegetables"
        )
        menu1.save()

        menu2 = Menu(
            restaurant=self.restaurant1,
            name="test menu 2",
            details="Corn Soup\nMixed vegetables Sandwich\nRoasted Vegetables"
        )
        self.assertRaisesRegex(
            IntegrityError, "UNIQUE constraint failed: restaurant_menu.restaurant_id, restaurant_menu.day",
            menu2.save
        )


class MenuSerializerTest(TestCase):

    def setUp(self):
        manager_instance = SelectorUser(
            username="manager",
            user_type=SelectorUser.RESTAURANT_MANAGER
        )
        manager_instance.save()

        restaurant = Restaurant(
            name="test restaurant", manager=manager_instance
        )
        restaurant.save()

        self.valid_menu_data = {
            "restaurant": restaurant.id,
            "name": "test restaurant",
            "details": "Corn Soup\nMixed vegetables Sandwich\nRoasted Vegetables"
        }

    def test_required_fields(self):
        fields = ["restaurant", "name", "details"]
        for field in fields:
            _data = copy.deepcopy(self.valid_menu_data)
            _data.pop(field)
            serializer = MenuSerializer(data=_data)
            self.assertEqual(serializer.is_valid(), False)
            self.assertRaisesRegex(
                DrfValidationError, f"{field}.*?This field is required",
                serializer.is_valid, raise_exception=True
            )

    def test_create_menu(self):
        serializer = MenuSerializer(data=self.valid_menu_data)
        self.assertEqual(serializer.is_valid(), True)
        menu = serializer.save()
        self.assertIsInstance(menu, Menu)

    def test_multiple_menu_same_day(self):
        serializer = MenuSerializer(data=self.valid_menu_data)
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        serializer = MenuSerializer(data=self.valid_menu_data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertRaisesRegex(
            AssertionError, r"You cannot call .*? on a serializer with invalid data.",
            serializer.save
        )
