"""
__WRISTBAND__: Template context processors for Wristband auth data context.
"""

from typing import Any, Dict

from django.http import HttpRequest


def wristband_auth(request: HttpRequest) -> Dict[str, Any]:
    """
    Add Wristband auth context to templates.

    Exposes session fields directly to templates (no nesting).

    Args:
        request: Django HTTP request with session middleware enabled.

    Returns:
        Context dictionary with auth data directly accessible in templates.

    Note:
        Excludes refresh_token for security reasons.
    """
    if not hasattr(request, "session"):
        return {}

    # Explicit list of fields used in demo templates
    session_fields = [
        "is_authenticated",
        "user_id",
        "tenant_id",
        "tenant_name",
        "tenant_custom_domain",
        "identity_provider_name",
        "email",
        "given_name",
        # ⚠️ DEMO ONLY - don't expose tokens in production templates
        "access_token",
    ]

    return {field: request.session.get(field) for field in session_fields if request.session.get(field) is not None}
