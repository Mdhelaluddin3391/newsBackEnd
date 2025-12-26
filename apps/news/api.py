from rest_framework import viewsets, permissions
from django.utils import timezone

from .models import Article
from .serializers import ArticleSerializer
from apps.users.permissions import IsEditor


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsEditor]

    def get_queryset(self):
        return Article.objects.filter(
            is_deleted=False
        ).select_related("author", "category")

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            status=Article.Status.DRAFT
        )
