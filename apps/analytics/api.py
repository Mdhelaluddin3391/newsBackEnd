from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.cache import cache

from .services import get_popular_articles, get_trending_articles
from .serializers import AnalyticsArticleSerializer


class PopularArticlesAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cache_key = "popular_articles"
        cached = cache.get(cache_key)

        if cached:
            return Response(cached)

        articles = get_popular_articles()
        data = AnalyticsArticleSerializer(articles, many=True).data
        cache.set(cache_key, data, 600)

        return Response(data)


class TrendingArticlesAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        days = int(request.query_params.get("days", 3))
        articles = get_trending_articles(days=days)
        data = AnalyticsArticleSerializer(articles, many=True).data
        return Response(data)
