"""
URL configuration for demo_app
"""

from django.urls import path

from . import views

app_name = "demo_app"

urlpatterns = [
    # __WRISTBAND__: Auth Endpoints
    path("api/auth/login/", views.login_endpoint, name="login"),
    path("api/auth/callback/", views.callback_endpoint, name="callback"),
    path("api/auth/logout/", views.logout_endpoint, name="logout"),
    # Page Views
    path("", views.HomePage.as_view(), name="home"),
    path("classic/", views.ClassicPage.as_view(), name="classic"),
    path("django-rest-framework/", views.DrfPage.as_view(), name="drf"),
    # Classic Django API Views
    path("api/classic/session-hello/", views.classic_session_hello_world_api, name="classic_session_hello"),
    path("api/classic/jwt-hello/", views.classic_jwt_hello_world_api, name="classic_jwt_hello"),
    # Django REST Framework (DRF) APIs
    path("api/drf/session/", views.SessionEndpoint.as_view(), name="drf_session"),
    path("api/drf/token/", views.TokenEndpoint.as_view(), name="drf_token"),
    path("api/drf/jwt-hello/", views.DrfJwtHelloApi.as_view(), name="drf_jwt_hello"),
]
