"""
Views for the demo app
"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class Home(View):
    """
    Home page view
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "demo_app/home.html")


class HelloWorld(View):
    """
    Hello World view (requires auth)
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "demo_app/hello_world.html")


class Profile(View):
    """
    User profile view (requires auth)
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "demo_app/profile.html")
