"""
API endpoints for the demo app
"""

import json
from datetime import datetime

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from wristband.django_auth import wristband_auth_required

from demo_app.wristband import wristband_jwt


@wristband_auth_required  # __WRISTBAND__: Protected View
@require_POST
def cookie_hello_world_api(request: HttpRequest) -> HttpResponse:
    """
    API endpoint using session-based authentication with cookies and CSRF protection.
    """

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


@csrf_exempt
@require_POST
def token_hello_world_api(request: HttpRequest) -> HttpResponse:
    """
    API endpoint using JWT bearer token authentication.
    """

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
        print(f"JWT validation error: {error}")
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
