from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification, NotificationPreference
from .serializers import (
    NotificationSerializer,
    NotificationPreferenceSerializer,
)


class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        ).order_by("-created_at")


class MarkNotificationReadAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        Notification.objects.filter(
            pk=pk,
            user=request.user
        ).update(is_read=True)

        return Response(
            {"detail": "Notification marked as read"},
            status=status.HTTP_200_OK
        )


class NotificationPreferenceAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        pref, _ = NotificationPreference.objects.get_or_create(
            user=self.request.user
        )
        return pref
