"""
API endpoints for the demo app
"""

import json
from datetime import datetime

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from demo_app.wristband import require_jwt, require_session


# __WRISTBAND__: Protected View
@require_session
@require_POST
def classic_session_hello_world_api(request: HttpRequest) -> HttpResponse:
    """
    API endpoint using session-based authentication with cookies and CSRF protection.
    """

    try:
        # Parse JSON body
        data = json.loads(request.body)
        action = data.get("action")

        if action != "hello":
            return JsonResponse({"error": 'Invalid action. Expected "hello".'}, status=400)

        response_data = {
            "message": "Hello World!",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        return JsonResponse(response_data, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)


# __WRISTBAND__: Protected View
@csrf_exempt
@require_jwt
@require_POST
def classic_jwt_hello_world_api(request: HttpRequest) -> HttpResponse:
    """
    API endpoint using JWT bearer token authentication.
    """
    try:
        print(request.user)
        # Parse JSON body
        data = json.loads(request.body)
        action = data.get("action")
        if action != "hello":
            return JsonResponse({"error": 'Invalid action. Expected "hello".'}, status=400)

        response_data = {"message": "Hello World!", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        return JsonResponse(response_data, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)
