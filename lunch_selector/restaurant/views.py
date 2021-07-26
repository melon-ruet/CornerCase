"""Restaurant related views"""
import logging

from rest_framework import viewsets

from restaurant.serializers import RestaurantSerializer
from user.models import SelectorUser

logger = logging.getLogger(__name__)


class RestaurantViewSet(viewsets.ModelViewSet):
    """Restaurant create, update, delete DRF views"""
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        objects = self.serializer_class.Meta.model.objects
        if self.request.user.user_type == SelectorUser.RESTAURANT_MANAGER:
            return objects.filter(manager=self.request.user.id)
        return objects.all()

    def initial(self, request, *args, **kwargs):
        """Add initial value before create or update"""
        user_type = getattr(request.user, "user_type", None)
        if user_type == SelectorUser.RESTAURANT_MANAGER:
            request.data["manager"] = request.user.id
        super().initial(request, *args, **kwargs)
