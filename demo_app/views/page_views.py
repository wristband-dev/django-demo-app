"""
Page Views for the demo app
"""

from django.views.generic import TemplateView

from demo_app.wristband import SessionRequiredMixin


class HomePage(TemplateView):
    """
    Home page
    """

    template_name = "demo_app/home.html"


# __WRISTBAND__: Protected View
class ClassicPage(SessionRequiredMixin, TemplateView):  # type: ignore
    """
    Hello World with Classic Django Views
    """

    template_name = "demo_app/classic.html"


# __WRISTBAND__: Protected View
class DrfPage(SessionRequiredMixin, TemplateView):  # type: ignore
    """
    Hello World with Django REST Framework APIs
    """

    template_name = "demo_app/drf.html"
