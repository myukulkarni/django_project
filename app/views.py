import random
from django.contrib.auth import get_user_model, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings  # ✅ required to access EMAIL_HOST_USER
from app.tasks import send_welcome_email,send_otp_email

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        name = request.data.get("name")
        username = request.data.get("username")
        email = request.data.get("email")
        phone = request.data.get("phone")
        password = request.data.get("password")

        if not all([name, username, email, phone, password]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        otp = str(random.randint(100000, 999999))
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                phone=phone,
                name=name,
                password=password,
                email_otp=otp,
                is_verified=False
            )

            # ✅ Send OTP using Celery task
            send_otp_email.delay(name, email, otp)

            return Response({
                "message": "User registered successfully. OTP sent to your email.",
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Failed to register: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ✅ OTP Verification View
class VerifyOTPView(APIView):
    def post(self, request, user_id):
        otp = request.data.get("otp")
        try:
            user = User.objects.get(id=user_id, email_otp=otp)
            user.is_verified = True
            user.email_otp = None
            user.save()

            # ✅ Send Welcome Email using Celery
            send_welcome_email.delay(user.email)

            return Response({"success": "Email verified successfully!"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Invalid OTP or User ID."}, status=status.HTTP_400_BAD_REQUEST)

# ✅ Login View (only if verified)
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            if not user.is_verified:
                return Response({"error": "Please verify your account first."}, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful.",
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class PublicView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "message": "Hello! This is a public endpoint. No authentication needed."
        })

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # request.user is guaranteed to be a valid, authenticated user
        return Response({
            "message": f"Hello {request.user.username}! You are authenticated and can see this protected data."
        })
