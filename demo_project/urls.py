"""
URL configuration for demo_project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpRequest, HttpResponse
from django.urls import include, path


def robots_txt(request: HttpRequest) -> HttpResponse:
    return HttpResponse("User-agent: *\nDisallow:", content_type="text/plain")


urlpatterns = [
    path("robots.txt", robots_txt),
    path("", include("demo_app.urls")),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
