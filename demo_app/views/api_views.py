"""
API endpoints for the demo app
"""

import json
from datetime import datetime

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View


class HelloWorldApi(View):
    """
    API endpoint example - accepts POST with JSON body
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
