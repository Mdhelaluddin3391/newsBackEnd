from rest_framework import viewsets, permissions

from .models import ArticleAnalytics
from .serializers import ArticleAnalyticsSerializer
from apps.users.permissions import IsAdmin, IsEditor


class ArticleAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ArticleAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated, IsEditor | IsAdmin]

    def get_queryset(self):
        return ArticleAnalytics.objects.filter(is_deleted=False)
