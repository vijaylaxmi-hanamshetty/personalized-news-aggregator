from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from Authentication.seralizers import RegisterSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from django.conf import settings
from Authentication.utils import send_sms
from drf_spectacular.utils import extend_schema, OpenApiResponse
from twilio.base.exceptions import TwilioRestException
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from rest_framework_simplejwt.tokens import RefreshToken 
User = get_user_model()

DEFAULT_REGION = 'IN'  

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

            try:
                parsed_number = phonenumbers.parse(user.phone, DEFAULT_REGION)
                if not phonenumbers.is_valid_number(parsed_number):
                    raise ValueError("Invalid phone number format.")
                formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

                message = f"Welcome {user.name}, your account has been successfully created."
                send_sms(formatted_number, message)

            except ValueError as ve:
                return Response({"detail": f"Invalid phone number: {str(ve)}"}, status=status.HTTP_400_BAD_REQUEST)
            except NumberParseException as npe:
                return Response({"detail": f"Phone number parsing error: {str(npe)}"}, status=status.HTTP_400_BAD_REQUEST)
            except TwilioRestException as e:
                return Response({"detail": f"Error sending SMS: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                access_token = str(refresh.access_token)
                refresh_token = str(refresh) 
                try:
                    parsed_number = phonenumbers.parse(phone, DEFAULT_REGION)  # None will use default region
                    if not phonenumbers.is_valid_number(parsed_number):
                        raise ValueError("Invalid phone number format.")
                    formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

                    message = f"Hello {user.name}, you have successfully logged in."
                    send_sms(formatted_number, message)

                except ValueError as ve:
                    return Response({"detail": f"Invalid phone number: {str(ve)}"}, status=status.HTTP_400_BAD_REQUEST)
                except NumberParseException as npe:
                    return Response({"detail": f"Phone number parsing error: {str(npe)}"}, status=status.HTTP_400_BAD_REQUEST)
                except TwilioRestException as e:
                    return Response({"detail": f"Error sending SMS: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response(
                    {
                        "message": "Login successful.",
                        "user": {
                            "id": user.id,
                            "phone": user.phone,
                            "name": user.name,
                            "role": user.role,
                        },
                        "access": access_token,  
                        "refresh": refresh_token,  
                    },
                    status=status.HTTP_200_OK,
                )
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
