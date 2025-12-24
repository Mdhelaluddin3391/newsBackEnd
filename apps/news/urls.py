from django.urls import path
from .api import (
    CategoryListAPIView,
    ArticleListAPIView,
    ArticleDetailAPIView,
    ArticleCreateAPIView,
    ArticleSubmitForReviewAPIView,
    ArticlePublishAPIView,
)

urlpatterns = [
    path("categories/", CategoryListAPIView.as_view()),

    path("articles/", ArticleListAPIView.as_view()),
    path("articles/<slug:slug>/", ArticleDetailAPIView.as_view()),

    path("articles/create/", ArticleCreateAPIView.as_view()),
    path("articles/<int:pk>/submit/", ArticleSubmitForReviewAPIView.as_view()),
    path("articles/<int:pk>/publish/", ArticlePublishAPIView.as_view()),
]
