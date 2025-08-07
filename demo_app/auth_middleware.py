import logging
from typing import Optional

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from .wristband import wristband_auth

logger = logging.getLogger(__name__)


class AuthMiddleware(MiddlewareMixin):
    API_PATH_PREFIX = "/api/"
    PUBLIC_PATH_PREFIXES = ["/auth/", "/static/"]
    PUBLIC_EXACT_PATHS = ["/", "/robots.txt"]

    def process_request(self, request: HttpRequest) -> Optional[HttpResponse]:
        path = request.path

        # Skip authentication for public paths
        if any(path.startswith(prefix) for prefix in self.PUBLIC_PATH_PREFIXES) or path in self.PUBLIC_EXACT_PATHS:
            logger.info(f"Skipping auth middleware for: {request.method} {path}")
            return None

        # __WRISTBAND__: Validate the user's authenticated session
        wristband_data = request.session.get("wristband")
        if not wristband_data:
            return self._auth_failure_response(request)

        try:
            # __WRISTBAND__: This will only refresh the token if it is truly expired.
            refresh_token = wristband_data.get("refresh_token")
            expires_at = wristband_data.get("expires_at", 0)
            new_token_data = wristband_auth.refresh_token_if_expired(refresh_token, expires_at)

            if new_token_data:
                # __WRISTBAND__: Update session with new token data
                wristband_data.update(
                    {
                        "access_token": new_token_data.access_token,
                        "refresh_token": new_token_data.refresh_token,
                        "id_token": new_token_data.id_token,
                        "expires_at": new_token_data.expires_at,
                    }
                )
                request.session["wristband"] = wristband_data

            # __WRISTBAND__: Need to call this here to update the CSRF cookie expiration time
            get_token(request)

        except Exception as e:
            logger.exception(f"Auth middleware error during token refresh: {str(e)}")
            return self._auth_failure_response(request)

        return None

    def _auth_failure_response(self, request: HttpRequest) -> HttpResponse:
        """Handle authentication failure by clearing session and returning appropriate response."""
        logger.info(f"Unauthenticated request to {request.path}")

        # __WRISTBAND__: Clear session
        request.session.flush()

        # Return 401 for API requests
        if request.path.startswith(self.API_PATH_PREFIX):
            return JsonResponse({"error": "Authentication failed"}, status=401)

        # Redirect to login for pages
        return redirect("/auth/login")
