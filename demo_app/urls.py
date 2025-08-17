"""
URL configuration for demo_app
"""

from django.urls import path

from . import views

app_name = "demo_app"

urlpatterns = [
    # Pages
    path("", views.Home.as_view(), name="home"),
    path("hello-world/", views.HelloWorld.as_view(), name="hello_world"),
    path("profile/", views.Profile.as_view(), name="profile"),
    # API Endpoints
    path("api/cookie-hello/", views.CookieHelloWorldApi.as_view(), name="api_cookie_hello"),
    path("api/token-hello/", views.TokenHelloWorldApi.as_view(), name="api_token_hello"),
    # __WRISTBAND__: Auth Endpoints
    path("auth/login/", views.Login.as_view(), name="login"),
    path("auth/callback/", views.Callback.as_view(), name="callback"),
    path("auth/logout/", views.Logout.as_view(), name="logout"),
]
