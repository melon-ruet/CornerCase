"""Voting related serializers"""
import datetime
import logging

from rest_framework import serializers

from vote.models import MenuVote

logger = logging.getLogger(__name__)


class MenuVoteSerializer(serializers.ModelSerializer):
    """Vote on menus by employees"""

    def create(self, validated_data):
        """Vote to menu"""
        logger.info(f"Vote given data: {validated_data}")
        return super().create(validated_data)

    def validate_menu(self, value):
        """validate menu"""
        if value.day != datetime.datetime.today().date():
            raise serializers.ValidationError("Menu is not from today")
        return value

    class Meta:  # pylint: disable=missing-class-docstring
        model = MenuVote
        fields = ("id", "menu", "day", "employee")
        read_only_fields = ("day",)
        extra_kwargs = {"employee": {"write_only": True}}
