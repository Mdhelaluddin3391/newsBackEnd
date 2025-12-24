from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from django.core.cache import cache

from .services import search_articles
from .serializers import SearchArticleSerializer


class SearchAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get("q")
        if not query:
            raise ValidationError({"q": "Search query is required"})

        cache_key = f"search:{query}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        results = search_articles(query)
        data = SearchArticleSerializer(results, many=True).data
        cache.set(cache_key, data, 300)

        return Response(data)
