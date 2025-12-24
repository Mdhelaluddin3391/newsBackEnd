from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from apps.core.permissions import IsOwnerOrReadOnly
from .models import Category, Article
from .serializers import (
    CategorySerializer,
    ArticleSerializer,
    ArticleCreateSerializer,
)
from .permissions import IsJournalistOrAbove, IsEditorOrAdmin


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@method_decorator(cache_page(60 * 5), name="dispatch")
class ArticleListAPIView(generics.ListAPIView):
    queryset = Article.objects.filter(status="published")
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ArticleDetailAPIView(generics.RetrieveAPIView):
    queryset = Article.objects.filter(status="published")
    serializer_class = ArticleSerializer
    lookup_field = "slug"


class ArticleCreateAPIView(generics.CreateAPIView):
    serializer_class = ArticleCreateSerializer
    permission_classes = [IsJournalistOrAbove]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleSubmitForReviewAPIView(generics.UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsJournalistOrAbove]

    def perform_update(self, serializer):
        serializer.save(status="review")


class ArticlePublishAPIView(generics.UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsEditorOrAdmin]

    def perform_update(self, serializer):
        serializer.save(
            status="published",
            published_at=timezone.now(),
        )


class ArticleUpdateAPIView(generics.UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer
    permission_classes = [IsJournalistOrAbove, IsOwnerOrReadOnly]
