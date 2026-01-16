"""
__WRISTBAND__: Wristband Django Auth SDK Configuration

This module initializes the Wristband authentication SDK and creates reusable
authentication decorators, mixins, and DRF authentication classes for your application.
"""

from django.conf import settings
from wristband.django_auth import (
    AuthConfig,
    AuthStrategy,
    UnauthenticatedBehavior,
    WristbandAuth,
)

__all__ = [
    "wristband_auth",
    "require_session",
    "require_jwt",
    "SessionRequiredMixin",
    "JwtRequiredMixin",
    "DrfSessionAuth",
    "DrfJwtAuth",
]

# ============================================================================
# Wristband Auth SDK Instance
# ============================================================================

wristband_auth = WristbandAuth(AuthConfig(**settings.WRISTBAND_AUTH))

# ============================================================================
# Function-Based View Decorators
# ============================================================================
# Use these decorators on Django function-based views to enforce authentication.
#
# Example:
#     @require_session
#     def dashboard(request):
#         return render(request, 'dashboard.html')

require_session = wristband_auth.create_auth_decorator(
    strategies=[AuthStrategy.SESSION],
    on_unauthenticated=UnauthenticatedBehavior.JSON,
)

require_jwt = wristband_auth.create_auth_decorator(
    strategies=[AuthStrategy.JWT],
    on_unauthenticated=UnauthenticatedBehavior.JSON,
)

# ============================================================================
# Class-Based View Mixins
# ============================================================================
# Use these mixins with Django class-based views to enforce authentication.
# The mixin must be the leftmost class in the inheritance chain.
#
# Example:
#     class DashboardView(SessionRequiredMixin, TemplateView):
#         template_name = 'dashboard.html'

SessionRequiredMixin = wristband_auth.create_auth_mixin(
    strategies=[AuthStrategy.SESSION],
    on_unauthenticated=UnauthenticatedBehavior.REDIRECT,
)

JwtRequiredMixin = wristband_auth.create_auth_mixin(
    strategies=[AuthStrategy.JWT],
    on_unauthenticated=UnauthenticatedBehavior.JSON,
)

# ============================================================================
# Django REST Framework (DRF) Authentication Classes
# ============================================================================
# Use these with DRF's authentication_classes to protect API endpoints.
#
# Example:
#     class SettingsView(APIView):
#         authentication_classes = [DrfJwtAuth]
#         permission_classes = [IsAuthenticated]

DrfSessionAuth = wristband_auth.create_drf_session_auth()

DrfJwtAuth = wristband_auth.create_drf_jwt_auth()
