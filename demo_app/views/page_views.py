"""
Views for the demo app
"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from wristband.django_auth import WristbandAuthRequiredMixin


class Home(View):
    """
    Home page view
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "demo_app/home.html")


class HelloWorld(WristbandAuthRequiredMixin, View):  # __WRISTBAND__: Protected View
    """
    Hello World view (requires auth)
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "demo_app/hello_world.html")


class Profile(WristbandAuthRequiredMixin, View):  # __WRISTBAND__: Protected View
    """
    User profile view (requires auth)
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "demo_app/profile.html")
