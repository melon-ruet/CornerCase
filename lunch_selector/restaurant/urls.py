"""Url collections of related to restaurant"""
from rest_framework import routers

from restaurant import views

router = routers.SimpleRouter()
router.register("", views.RestaurantViewSet, basename="restaurant")
router.register("menus", views.MenuViewSet, basename="menu")
urlpatterns = router.urls
