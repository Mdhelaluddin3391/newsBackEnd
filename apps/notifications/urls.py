from django.urls import path
from .api import (
    NotificationListAPIView,
    MarkNotificationReadAPIView,
    NotificationPreferenceAPIView,
)

urlpatterns = [
    path("", NotificationListAPIView.as_view()),
    path("<int:pk>/read/", MarkNotificationReadAPIView.as_view()),
    path("preferences/", NotificationPreferenceAPIView.as_view()),
]
