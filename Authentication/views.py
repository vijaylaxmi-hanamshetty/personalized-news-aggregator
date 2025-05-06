from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from Authentication.seralizers import RegisterSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@extend_schema(
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(description="Registration successful.", response=RegisterSerializer),
        400: OpenApiResponse(description="Bad request. Validation failed."),
    },
)
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "Registration successful.",
                    "user": RegisterSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@extend_schema(
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            description="Login successful.",
            response={
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "user": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "phone": {"type": "string"},
                            "name": {"type": "string"},
                            "role": {"type": "string"},
                        },
                    },
                    "access": {"type": "string"},
                    "refresh": {"type": "string"},
                },
            },
        ),
        400: OpenApiResponse(description="Invalid credentials."),
    },
)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data["phone"]
            password = serializer.validated_data["password"]
            user = User.objects.filter(phone=phone).first()

            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "message": "Login successful.",
                        "user": {
                            "id": user.id,
                            "phone": user.phone,
                            "name": user.name,
                            "role": user.role,
                        },
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                    },
                    status=status.HTTP_200_OK,
                )

            return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
