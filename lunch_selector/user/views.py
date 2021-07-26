"""User related views"""
import logging

from rest_framework import generics

from user.permissions import SuperuserPermission
from user.serializers import UserSerializer

logger = logging.getLogger(__name__)


class UserCreateView(generics.CreateAPIView):
    """User creation DRF view"""
    serializer_class = UserSerializer
    permission_classes = [SuperuserPermission]
