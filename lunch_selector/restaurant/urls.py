"""Url collections of related to restaurant"""
from rest_framework import routers

from restaurant import views

router = routers.SimpleRouter()
router.register("menus", views.MenuViewSet, basename="menu")
router.register("", views.RestaurantViewSet, basename="restaurant")
urlpatterns = router.urls
