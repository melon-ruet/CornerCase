"""User related serializers"""
import logging

from django.contrib.auth import password_validation as validators, get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.utils.representation import smart_repr

from .models import SelectorUser

logger = logging.getLogger(__name__)
UserModel = get_user_model()


class PasswordValidator:
    """Password match validator"""
    message = _("{password_field} should be equal to {confirm_password_field}.")

    def __init__(self, password_field="password", confirm_password_field="confirm_password",
                 message=None):
        self.password_field = password_field
        self.confirm_password_field = confirm_password_field
        self.message = message or self.message

    def __call__(self, attrs):
        if attrs[self.password_field] != attrs[self.confirm_password_field]:
            message = self.message.format(
                password_field=self.password_field,
                confirm_password_field=self.confirm_password_field,
            )
            raise serializers.ValidationError(message, code="password_mismatch")

    def __repr__(self):
        return "<%s(password_field=%s, confirm_password_field=%s)>" % (
            self.__class__.__name__,
            smart_repr(self.password_field),
            smart_repr(self.confirm_password_field)
        )


class UserSerializer(serializers.ModelSerializer):
    """UserSerializer for creating user with a password"""
    password_max_len = UserModel._meta.get_field("password").max_length
    password = serializers.CharField(
        label=_("Password"), max_length=password_max_len, write_only=True
    )
    confirm_password = serializers.CharField(
        label=_("Confirm password"), max_length=password_max_len, write_only=True
    )

    def validate_password(self, value):
        """Validate password value with default password validators"""
        logger.info("Validating user password")
        validators.validate_password(password=value)
        return value

    def create(self, validated_data):
        """Create user after validation all"""
        validated_data.pop("confirm_password")
        user = UserModel.objects.create_user(**validated_data)
        logger.info(f"User created: {user.username}")
        return user

    class Meta:
        model = SelectorUser
        validators = [PasswordValidator()]
        fields = (
            "id", "username", "first_name", "last_name", "email", "password", "confirm_password"
        )
