from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(
            is_deleted=False
        ).select_related("user", "article")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def edit(self, request, pk=None):
        comment = self.get_object()
        new_content = request.data.get("content")

        try:
            comment.edit(new_content)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(CommentSerializer(comment).data)

    @action(detail=True, methods=["post"])
    def report(self, request, pk=None):
        comment = self.get_object()
        comment.report()
        return Response({"detail": "Comment reported successfully"})
