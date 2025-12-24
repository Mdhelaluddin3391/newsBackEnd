from django.urls import path
from .api import CommentListAPIView, CommentCreateAPIView

urlpatterns = [
    path(
        "article/<int:article_id>/",
        CommentListAPIView.as_view(),
    ),
    path(
        "create/",
        CommentCreateAPIView.as_view(),
    ),
]
