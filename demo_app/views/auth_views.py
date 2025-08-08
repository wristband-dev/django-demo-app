import logging

from django.http import HttpRequest, HttpResponse
from django.middleware.csrf import get_token
from django.views import View
from wristband.django_auth import CallbackData, CallbackResultType, LogoutConfig

from ..wristband import wristband_auth

logger = logging.getLogger(__name__)


class Login(View):
    """
    Construct the authorize request URL and redirect to the Wristband Authorize Endpoint
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        return wristband_auth.login(request)  # __WRISTBAND__


class Callback(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Wristband SDK will fetch token and user data after the user authenticates, store them
        into a new session, and then this view will redirect into the application.
        """
        callback_result = wristband_auth.callback(request)  # __WRISTBAND__

        # Some edges require an immediate redirect to restart the login flow
        if callback_result.type == CallbackResultType.REDIRECT_REQUIRED:
            redirect_url: str = callback_result.redirect_url  # type: ignore[assignment]
            return wristband_auth.create_callback_response(request, redirect_url)

        # Store session data for authenticated user
        callback_data: CallbackData = callback_result.callback_data  # type: ignore[assignment]
        request.session["wristband"] = {
            "user_info": callback_data.user_info,
            "access_token": callback_data.access_token,
            "refresh_token": callback_data.refresh_token,
            "expires_at": callback_data.expires_at,
            "tenant_domain_name": callback_data.tenant_domain_name,
            "tenant_custom_domain": callback_data.tenant_custom_domain,
        }

        # This creates the csrftoken cookie and stores the token in the session.
        get_token(request)

        # Redirect to return URL, if present; otherwise default to Home page.
        post_callback_url = callback_data.return_url or "/"
        return wristband_auth.create_callback_response(request, post_callback_url)


class Logout(View):
    """
    Log out the user and redirect to the Wristband Logout Endpoint.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        # Get session data
        wristband_session = request.session.get("wristband", {})
        refresh_token = wristband_session.get("refresh_token")
        tenant_domain_name = wristband_session.get("tenant_domain_name")
        tenant_custom_domain = wristband_session.get("tenant_custom_domain")

        # Wristband SDK revokes the refresh token and creates the proper redirect response
        logout_config = LogoutConfig(
            refresh_token=refresh_token,  # Pass in the refresh token you want to revoke
            tenant_domain_name=tenant_domain_name,  # Wristband Logout requires a tenant level domain
            tenant_custom_domain=tenant_custom_domain,  # Custom domains take precedence, if present
            redirect_url="http://localhost:6001",  # Redirect to home page
        )
        response = wristband_auth.logout(request, logout_config)  # __WRISTBAND__

        # Clear the session as well as CSRF cookie
        request.session.flush()
        response.delete_cookie("csrftoken")

        return response
