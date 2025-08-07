"""
__WRISTBAND__: Wristband Django Auth SDK Configuration
"""

from django.conf import settings
from wristband.django_auth import AuthConfig, WristbandAuth

__all__ = ["wristband_auth"]


def _create_wristband_auth() -> WristbandAuth:
    wristband_settings = settings.WRISTBAND_AUTH

    auth_config = AuthConfig(
        client_id=wristband_settings["client_id"],
        client_secret=wristband_settings["client_secret"],
        wristband_application_vanity_domain=wristband_settings["wristband_application_vanity_domain"],
        login_url=wristband_settings["login_url"],
        redirect_uri=wristband_settings["redirect_uri"],
        login_state_secret=wristband_settings["login_state_secret"],
        dangerously_disable_secure_cookies=wristband_settings.get("dangerously_disable_secure_cookies"),
    )
    return WristbandAuth(auth_config)


wristband_auth: WristbandAuth = _create_wristband_auth()
