"""lunch_selector URL Configuration"""
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from rest_framework.authtoken.views import obtain_auth_token

schema_view = get_schema_view(
    openapi.Info(
        title="Lunch Selector API",
        default_version="v1",
        description="Endpoints of Lunch Selector application",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("token/", obtain_auth_token),
    path("user/", include("user.urls")),
    path("restaurants/", include("restaurant.urls")),
    path("votes", include("vote.urls")),
]
