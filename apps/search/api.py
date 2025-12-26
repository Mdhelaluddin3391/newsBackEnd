from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from django.core.cache import cache
from .services import search_articles
from .serializers import SearchArticleSerializer

class SearchAPIView(APIView):
    """Grounded in PostgreSQL Full-Text Search"""
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get("q")
        if not query:
            raise ValidationError({"q": "Search query is required"})

        # Performance ke liye cache check karein
        cache_key = f"search:{query}"
        cached_results = cache.get(cache_key)
        
        if cached_results:
            return Response(cached_results)

        results = search_articles(query)
        data = SearchArticleSerializer(results, many=True).data
        
        # 5 minute ke liye results cache karein
        cache.set(cache_key, data, 300) 
        return Response(data)