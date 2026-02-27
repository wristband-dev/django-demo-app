from datetime import datetime

from django.http import HttpRequest
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Empty, Request
from rest_framework.response import Response
from rest_framework.views import APIView
from wristband.django_auth import JWTAuthResult, get_session_response, get_token_response

from demo_app.wristband import DrfJwtAuth, DrfSessionAuth


class SessionEndpoint(APIView):
    """Returns session information - uses session auth."""

    authentication_classes = [DrfSessionAuth]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        email = request.session.get("email")
        session_data = get_session_response(request._request, metadata={"email": email})
        return Response(session_data.to_dict())


class TokenEndpoint(APIView):
    """Returns access token - uses session auth."""

    authentication_classes = [DrfSessionAuth]
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> Response:
        token_data = get_token_response(request)
        return Response(token_data.to_dict())


class DrfJwtHelloApi(APIView):
    """DRF API endpoint using Wristband JWT authentication."""

    authentication_classes = [DrfJwtAuth]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        if isinstance(request.data, Empty):
            return Response({"error": "Request body is required."}, status=status.HTTP_400_BAD_REQUEST)

        action = request.data.get("action")

        if action != "hello":
            return Response({"error": 'Invalid action. Expected "hello".'}, status=status.HTTP_400_BAD_REQUEST)

        assert isinstance(request.auth, JWTAuthResult)  # nosec B101

        return Response(
            {
                "message": "Hello World from DRF JWT!",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "userId": request.auth.payload.get("sub"),
                "tenantId": request.auth.payload.get("tnt_id"),
            }
        )
