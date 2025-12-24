from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer


class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            article_id=self.kwargs["article_id"],
            parent__isnull=True,
            is_active=True,
        )


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
