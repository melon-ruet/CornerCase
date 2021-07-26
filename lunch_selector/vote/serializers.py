"""Voting related serializers"""
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

    class Meta:
        model = MenuVote
        fields = ("id", "menu", "day", "employee")
        read_only_fields = ("day",)
        extra_kwargs = {"employee": {"write_only": True}}
