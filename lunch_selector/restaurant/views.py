"""Restaurant related views"""
import datetime
import logging

from rest_framework import viewsets, status
from rest_framework.response import Response

from restaurant.serializers import RestaurantSerializer, MenuSerializer
from user.models import SelectorUser

logger = logging.getLogger(__name__)


class RestaurantViewSet(viewsets.ModelViewSet):
    """Restaurant create, update, delete DRF views"""
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        """get restaurants based on user type"""
        objects = self.serializer_class.Meta.model.objects
        user_type = getattr(self.request.user, "user_type", None)
        if user_type is None:
            return objects.none()
        if user_type == SelectorUser.RESTAURANT_MANAGER:
            return objects.filter(manager=self.request.user.id)
        return objects.all()

    def initial(self, request, *args, **kwargs):
        """Add initial value before create or update"""
        user_type = getattr(request.user, "user_type", None)
        if user_type == SelectorUser.RESTAURANT_MANAGER:
            request.data["manager"] = request.user.id
        super().initial(request, *args, **kwargs)


class MenuViewSet(viewsets.ModelViewSet):
    """Menu create, update, delete DRF views"""
    serializer_class = MenuSerializer

    def get_queryset(self):
        """Get menus by user type"""
        objects = self.serializer_class.Meta.model.objects
        user_type = getattr(self.request.user, "user_type", None)
        if user_type == SelectorUser.EMPLOYEE:
            return objects.filter(
                day=datetime.datetime.today()
            )
        if user_type == SelectorUser.RESTAURANT_MANAGER:
            return objects.filter(restaurant__manager=self.request.user)
        return objects.all()

    def create(self, request, *args, **kwargs):
        """Override to check if proper restaurant id provided"""
        if request.user.user_type == SelectorUser.RESTAURANT_MANAGER:
            restaurants = RestaurantSerializer.Meta.model.objects.filter(
                manager=request.user
            )
            if request.data.get("restaurant", None) not in \
                    restaurants.values_list("id", flat=True):
                return Response(
                    "Invalid restaurant ID",
                    status=status.HTTP_400_BAD_REQUEST
                )

        return super().create(request, *args, **kwargs)
