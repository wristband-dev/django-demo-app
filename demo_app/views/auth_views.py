from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.http import require_GET
from wristband.django_auth import LogoutConfig, RedirectRequiredCallbackResult, session_from_callback

from ..wristband import wristband_auth


@require_GET
def login_endpoint(request: HttpRequest) -> HttpResponse:
    """Construct the authorize request URL and redirect to the Wristband Authorize Endpoint."""
    return wristband_auth.login(request)  # __WRISTBAND__


@require_GET
def callback_endpoint(request: HttpRequest) -> HttpResponse:
    """
    Wristband SDK will fetch token and user data after the user authenticates, store them
    into a new session, and then this view will redirect into the application.
    """
    callback_result = wristband_auth.callback(request)  # __WRISTBAND__

    # Some edges require an immediate redirect to restart the login flow
    if isinstance(callback_result, RedirectRequiredCallbackResult):
        return wristband_auth.create_callback_response(request, callback_result.redirect_url)

    # Store session data for authenticated user
    callback_data = callback_result.callback_data
    session_from_callback(
        request=request,
        callback_data=callback_data,
        custom_fields={"email": callback_data.user_info.email, "given_name": callback_data.user_info.given_name},
    )

    # Django's auth system: WristbandAuthBackend handles user syncing with custom adapter
    user = authenticate(request, callback_data=callback_data)
    login(request, user)

    # This creates the csrftoken cookie and stores the token in the session.
    get_token(request)

    # Redirect to return URL, if present; otherwise default to Home page.
    post_callback_url = callback_data.return_url or "/"
    return wristband_auth.create_callback_response(request, post_callback_url)


@require_GET
def logout_endpoint(request: HttpRequest) -> HttpResponse:
    """Log out the user and redirect to the Wristband Logout Endpoint."""
    # Wristband SDK revokes the refresh token and creates the proper redirect response
    logout_config = LogoutConfig(
        refresh_token=request.session.get("refresh_token"),  # The refresh token you want to revoke
        tenant_name=request.session.get("tenant_name"),  # Wristband Logout requires a tenant level domain
        tenant_custom_domain=request.session.get("tenant_custom_domain"),  # Custom domains takes precedence, if present
    )
    response = wristband_auth.logout(request, logout_config)  # __WRISTBAND__

    logout(request)  # Log user out of Django's auth system

    # Clear the session as well as CSRF cookie
    request.session.flush()
    response.delete_cookie("csrftoken")

    return response
