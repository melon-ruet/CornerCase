"""Url collections of related to user"""
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from user import views

urlpatterns = [
    path("token/", obtain_auth_token, name="token"),
    path("logout/", views.UserLogout.as_view(), name="logout"),
    path("", views.UserCreateView.as_view(), name="user-create"),
]
