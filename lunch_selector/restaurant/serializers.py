"""Restaurant related serializers"""
import logging

from rest_framework import serializers

from restaurant.models import Restaurant, Menu

logger = logging.getLogger(__name__)


class RestaurantSerializer(serializers.ModelSerializer):
    """RestaurantSerializer for create and list restaurants"""

    def create(self, validated_data):
        """Create user after validation all"""
        logger.info(f"Restaurant creation data: {validated_data}")
        return super().create(validated_data)

    class Meta:  # pylint: disable=missing-class-docstring
        model = Restaurant
        fields = ("id", "name", "manager")
        extra_kwargs = {"manager": {"write_only": True}}


class MenuSerializer(serializers.ModelSerializer):
    """MenuSerializer for CRUD menus"""

    def create(self, validated_data):
        """Create menu by restaurant manager"""
        logger.info(f"Menu creation data: {validated_data}")
        return super().create(validated_data)

    class Meta:  # pylint: disable=missing-class-docstring
        model = Menu
        fields = ("id", "restaurant", "name", "details", "day")
        extra_kwargs = {"restaurant": {"write_only": True}}
