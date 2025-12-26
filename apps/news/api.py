from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.utils import timezone
from .models import Category, Article
from .serializers import CategorySerializer, ArticleSerializer, ArticleCreateSerializer
from .permissions import IsJournalistOrAbove, IsEditorOrAdmin
from apps.core.permissions import IsOwnerOrReadOnly

class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ArticleListAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Article.objects.filter(status="published").order_by('-published_at')

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
    permission_classes = [IsJournalistOrAbove, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(status="review")

class ArticlePublishAPIView(generics.UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsEditorOrAdmin]

    def perform_update(self, serializer):
        article = serializer.save(status="published", published_at=timezone.now())
        
        # Notify the author
        notify(
            user=article.author,
            title="Article Published!",
            message=f"Your article '{article.title}' is now live.",
            type="news"
        )