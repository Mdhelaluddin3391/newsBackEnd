from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import EmailVerificationToken
from apps.notifications.services import send_html_email
from apps.core.models import BrandSettings

from .models import User
from .serializers import UserSerializer
from .permissions import IsAdmin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from apps.core.utils import create_audit_log


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from apps.core.utils import create_audit_log


EDITOR_DOMAIN = "yournews.com"



from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from apps.core.utils import create_audit_log
from django.urls import reverse
from django.conf import settings

from .models import PasswordResetToken
from apps.notifications.services import send_password_reset_email

class ForgotPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"detail": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email=email, is_active=True).first()

        # ⚠️ Do NOT reveal whether user exists
        if user:
            token_obj = PasswordResetToken.create_token(user)

            reset_link = (
                f"{settings.FRONTEND_URL}/reset-password/"
                f"{token_obj.token}"
            )

            send_password_reset_email(
                email=user.email,
                reset_link=reset_link
            )

            create_audit_log(
                user=user,
                action="UPDATE",
                model_name="User",
                object_id=user.id,
                description="Password reset requested"
            )

        return Response(
            {"detail": "If the email exists, a reset link has been sent"},
            status=status.HTTP_200_OK
        )



class ResetPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        if not token or not new_password:
            return Response(
                {"detail": "Token and new password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        token_obj = PasswordResetToken.objects.filter(
            token=token,
            used=False
        ).select_related("user").first()

        if not token_obj or not token_obj.is_valid():
            return Response(
                {"detail": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = token_obj.user
        user.set_password(new_password)
        user.save(update_fields=["password", "updated_at"])

        token_obj.mark_used()

        create_audit_log(
            user=user,
            action="UPDATE",
            model_name="User",
            object_id=user.id,
            description="Password reset successful"
        )

        return Response(
            {"detail": "Password reset successful"},
            status=status.HTTP_200_OK
        )




class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response(
                    {"detail": "Refresh token required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            create_audit_log(
                user=request.user,
                action="LOGOUT",
                model_name="User",
                object_id=request.user.id,
                description="User logged out"
            )

            return Response(
                {"detail": "Logged out successfully"},
                status=status.HTTP_200_OK
            )

        except TokenError:
            return Response(
                {"detail": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )



class GoogleLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get("token")

        if not token:
            return Response(
                {"detail": "Google token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # ✅ Verify Google ID token
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

            email = idinfo.get("email")
            full_name = idinfo.get("name", "")

            if not email:
                return Response(
                    {"detail": "Email not provided by Google"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            domain = email.split("@")[-1].lower()

            # 🔐 ROLE DECISION LOGIC
            if domain == EDITOR_DOMAIN:
                role = User.Role.EDITOR
            else:
                role = User.Role.USER

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "full_name": full_name,
                    "role": role,
                    "is_active": True,
                }
            )

            # 🔁 If user already exists but role not set properly
            if not created and user.role == User.Role.USER and domain == EDITOR_DOMAIN:
                user.role = User.Role.EDITOR
                user.save(update_fields=["role", "updated_at"])

            # 🔑 JWT tokens
            refresh = RefreshToken.for_user(user)

            # 🧾 Audit log
            create_audit_log(
                user=user,
                action="LOGIN",
                model_name="User",
                object_id=user.id,
                description=f"Google login ({user.role})"
            )

            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "full_name": user.full_name,
                        "role": user.role,
                    }
                },
                status=status.HTTP_200_OK
            )

        except ValueError:
            return Response(
                {"detail": "Invalid Google token"},
                status=status.HTTP_400_BAD_REQUEST
            )



class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]






class EmailSignupAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        full_name = request.data.get("full_name")

        if not email or not password or not full_name:
            return Response(
                {"detail": "Email, password and full name are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"detail": "User already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            email=email,
            password=password,
            full_name=full_name,
            role=User.Role.USER,
            is_active=True,
        )

        refresh = RefreshToken.for_user(user)

        create_audit_log(
            user=user,
            action="CREATE",
            model_name="User",
            object_id=user.id,
            description="Email signup"
        )

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role,
                }
            },
            status=status.HTTP_201_CREATED
        )



class EmailLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"detail": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if not user:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {"detail": "Account disabled"},
                status=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(user)

        create_audit_log(
            user=user,
            action="LOGIN",
            model_name="User",
            object_id=user.id,
            description="Email login"
        )

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role,
                }
            },
            status=status.HTTP_200_OK
        )



class SendVerificationEmailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.email_verified:
            return Response(
                {"detail": "Email already verified"},
                status=status.HTTP_400_BAD_REQUEST
            )

        token_obj = EmailVerificationToken.create_token(user)

        brand = BrandSettings.objects.first()

        verify_link = f"{brand.frontend_url}/verify-email/{token_obj.token}"

        send_html_email(
            subject="Verify your email",
            to_email=user.email,
            template_name="emails/email_verification.html",
            context={
                "user_name": user.full_name,
                "verify_link": verify_link,
            }
        )

        return Response(
            {"detail": "Verification email sent"},
            status=status.HTTP_200_OK
        )
class VerifyEmailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get("token")

        token_obj = EmailVerificationToken.objects.filter(
            token=token,
            verified=False
        ).select_related("user").first()

        if not token_obj or not token_obj.is_valid():
            return Response(
                {"detail": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = token_obj.user
        user.email_verified = True
        user.save(update_fields=["email_verified"])

        token_obj.verified = True
        token_obj.save(update_fields=["verified"])

        return Response(
            {"detail": "Email verified successfully"},
            status=status.HTTP_200_OK
        )
