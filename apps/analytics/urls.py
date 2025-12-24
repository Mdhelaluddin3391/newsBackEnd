from django.urls import path
from .api import PopularArticlesAPIView, TrendingArticlesAPIView

urlpatterns = [
    path("popular/", PopularArticlesAPIView.as_view()),
    path("trending/", TrendingArticlesAPIView.as_view()),
]
