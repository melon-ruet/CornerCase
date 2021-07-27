"""Url collections of related to vote"""
from rest_framework import routers

from vote import views

router = routers.SimpleRouter()
router.register("", views.MenuVoteViewSet, basename="vote")
urlpatterns = router.urls
