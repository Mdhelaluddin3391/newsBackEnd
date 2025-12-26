from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import CommentViewSet

router = DefaultRouter()
router.register("comments", CommentViewSet, basename="comments")

urlpatterns = [
    path("", include(router.urls)),
]
