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
        return Restaurant.objects.create(**validated_data)

    class Meta:
        model = Restaurant
        fields = ("id", "name", "manager")
        extra_kwargs = {"manager": {"write_only": True}}
