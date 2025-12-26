from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import ArticleAnalyticsViewSet

router = DefaultRouter()
router.register("articles", ArticleAnalyticsViewSet, basename="article-analytics")

urlpatterns = [
    path("", include(router.urls)),
]
