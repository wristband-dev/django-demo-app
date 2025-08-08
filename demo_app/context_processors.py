"""
__WRISTBAND__: Template context processors for Wristband auth data context.
"""

from typing import Any, Dict

from django.http import HttpRequest


def wristband_auth(request: HttpRequest) -> Dict[str, Any]:
    """
    Add Wristband auth context to templates

    This is an example context processor using Django sessions.
    Developers would adapt this to their chosen storage mechanism.

    Args:
        request: Django HTTP request

    Returns:
        Context dictionary with auth data
    """
    return {
        "wristband": request.session.get("wristband", {}),
    }
