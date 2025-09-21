from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsManager
from rest_framework.permissions import AllowAny
from rest_framework import status, generics
from django.contrib.auth.models import User
from .serializers import RegisterUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse


# Create your views here.

@extend_schema(
    tags=["Authentication"],
    request=RegisterUserSerializer,
    responses={201: RegisterUserSerializer},
    examples=[
        OpenApiExample(
            "Register Example",
            value={"username": "huraira", "group":"Manager / Employee", "email": "huraira@example.com", "password": "password123"},
        ),
    ],
)
class RegisterApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            "message": "User registered successfully.",
            "user": response.data
        }
        return response

@extend_schema(
    tags=["Authentication"],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "refresh": {"type": "string", "example": "your-refresh-token-here"}
            },
            "required": ["refresh"],
        }
    },
    responses={
        205: OpenApiResponse(
            description="Logout successful",
            examples=[
                OpenApiExample(
                    "Logout Example",
                    value={"message": "Logout successful.",}
                )
            ],
        ),
        400: OpenApiResponse(
            description="Invalid or missing token",
            examples=[
                OpenApiExample(
                    "Error Example",
                    value={"error": "Invalid or expired token."}
                )
            ],
        ),
    },
)
class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh)
            token.blacklist()
            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

