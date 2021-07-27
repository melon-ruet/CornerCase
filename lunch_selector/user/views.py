"""User related views"""
import logging

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.permissions import AdminPermission
from user.serializers import UserSerializer

logger = logging.getLogger(__name__)


class UserCreateView(generics.CreateAPIView):
    """User creation DRF view"""
    serializer_class = UserSerializer
    permission_classes = [AdminPermission]


class FakeLogoutSerializer:
    """Fake serializer for drf swagger view
    So it will not generate this log:
    ```AssertionError: 'UserLogout' should either include a
    `serializer_class` attribute, or override the `get_serializer_class()` method.```
    """
    def __call__(self, *args, **kwargs):
        pass


class UserLogout(generics.CreateAPIView):
    """User logout"""
    permission_classes = [IsAuthenticated]
    serializer_class = FakeLogoutSerializer()

    def create(self, request, *args, **kwargs):
        """Delete user token to logout"""
        request.user.auth_token.delete()
        return Response("You are logged out", status=status.HTTP_200_OK)
