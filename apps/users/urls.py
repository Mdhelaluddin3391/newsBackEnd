from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import UserViewSet, GoogleLoginAPIView

router = DefaultRouter()
router.register("", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/google/", GoogleLoginAPIView.as_view(), name="google-login"),
]


from .api import LogoutAPIView

urlpatterns += [
    path("auth/logout/", LogoutAPIView.as_view(), name="logout"),
]


from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api import (
    UserViewSet,
    GoogleLoginAPIView,
    EmailSignupAPIView,
    EmailLoginAPIView,
    LogoutAPIView,
)

router = DefaultRouter()
router.register("", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),

    # 🔐 Auth APIs
    path("auth/signup/", EmailSignupAPIView.as_view(), name="email-signup"),
    path("auth/login/", EmailLoginAPIView.as_view(), name="email-login"),
    path("auth/google/", GoogleLoginAPIView.as_view(), name="google-login"),
    path("auth/logout/", LogoutAPIView.as_view(), name="logout"),
]


from .api import ForgotPasswordAPIView, ResetPasswordAPIView

urlpatterns += [
    path("auth/forgot-password/", ForgotPasswordAPIView.as_view(), name="forgot-password"),
    path("auth/reset-password/", ResetPasswordAPIView.as_view(), name="reset-password"),
]
urlpatterns += [
    path("auth/send-verification/", SendVerificationEmailAPIView.as_view()),
    path("auth/verify-email/", VerifyEmailAPIView.as_view()),
]
