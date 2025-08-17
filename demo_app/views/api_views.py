"""
API endpoints for the demo app
"""

import json
from datetime import datetime

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from demo_app.wristband import wristband_jwt


class CookieHelloWorldApi(View):
    """
    API endpoint using session-based authentication with cookies and CSRF protection.
    """

    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            # Parse JSON body
            data = json.loads(request.body)
            action = data.get("action")

            if action != "hello":
                return JsonResponse({"error": 'Invalid action. Expected "hello".'}, status=400)

            response_data = {"message": "Hello World!", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            return JsonResponse(response_data, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class TokenHelloWorldApi(View):
    """
    API endpoint using JWT bearer token authentication.
    """

    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            # __WRISTBAND__: Wristband Python JWT SDK usage
            auth_header = request.META.get("HTTP_AUTHORIZATION")
            token = wristband_jwt.extract_bearer_token(auth_header)
            result = wristband_jwt.validate(token)

            if not result.is_valid:
                print(f"JWT validation failed: {result.error_message}")
                return HttpResponse(status=401)

            print(f"JWT Validation success for user with ID: [{result.payload.sub}]")  # type: ignore
        except Exception as error:
            print(f"JWT validation middleware error: {error}")
            return HttpResponse(status=401)

        try:
            # Parse JSON body
            data = json.loads(request.body)
            action = data.get("action")
            if action != "hello":
                return JsonResponse({"error": 'Invalid action. Expected "hello".'}, status=400)

            response_data = {"message": "Hello World!", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            return JsonResponse(response_data, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)
