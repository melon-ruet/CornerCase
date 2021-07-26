"""Url collections of related to user"""
from django.urls import path

from user import views

urlpatterns = [
    path("user", views.UserCreateView.as_view(), name="user-create"),
]
