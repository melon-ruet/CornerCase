"""lunch_selector URL Configuration"""
# from django.contrib import admin
from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from user.views import UserCreateView

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("token/", obtain_auth_token),
    path("user/", UserCreateView.as_view()),
]
