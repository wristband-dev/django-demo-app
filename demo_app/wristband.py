"""
__WRISTBAND__: Wristband Django Auth SDK and Python JWT Configuration
"""

from django.conf import settings
from wristband.django_auth import AuthConfig, WristbandAuth
from wristband.python_jwt import WristbandJwtValidator, WristbandJwtValidatorConfig, create_wristband_jwt_validator

__all__ = ["wristband_auth", "wristband_jwt"]

wristband_settings = settings.WRISTBAND_AUTH


# Wristband FastAPI Auth SDK Configuration
wristband_auth: WristbandAuth = WristbandAuth(
    AuthConfig(
        client_id=wristband_settings["client_id"],
        client_secret=wristband_settings["client_secret"],
        wristband_application_vanity_domain=wristband_settings["wristband_application_vanity_domain"],
        login_url=wristband_settings["login_url"],
        redirect_uri=wristband_settings["redirect_uri"],
        login_state_secret=wristband_settings["login_state_secret"],
    )
)

# Wristband Python JWT SDK Configuration
wristband_jwt: WristbandJwtValidator = create_wristband_jwt_validator(
    WristbandJwtValidatorConfig(
        wristband_application_vanity_domain=wristband_settings["wristband_application_vanity_domain"],
    )
)
