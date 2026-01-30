"""
URL configuration for demo_project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import include, path


def robots_txt(request: HttpRequest) -> HttpResponse:
    return HttpResponse("User-agent: *\nDisallow:", content_type="text/plain")


def admin_login_redirect(request: HttpRequest) -> HttpResponse:
    """Redirect admin login to Wristband"""
    return_url = request.build_absolute_uri("/admin/")
    return redirect(f"/api/auth/login/?return_url={return_url}")


def admin_logout_redirect(request: HttpRequest) -> HttpResponse:
    """Redirect admin logout to Wristband"""
    return_url = request.build_absolute_uri("/admin/")
    return redirect(f"/api/auth/logout/?return_url={return_url}")


urlpatterns = [
    path("admin/login/", admin_login_redirect),
    path("admin/logout/", admin_logout_redirect),
    path("admin/", admin.site.urls),
    path("robots.txt", robots_txt),
    path("", include("demo_app.urls")),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
