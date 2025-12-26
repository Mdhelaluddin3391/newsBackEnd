from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .services import SearchService
from .serializers import SearchResultSerializer


class SearchAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get("q")
        category = request.query_params.get("category")
        article_type = request.query_params.get("type")

        results = SearchService.search(
            query=query,
            category=category,
            article_type=article_type,
        )

        serializer = SearchResultSerializer(results, many=True)
        return Response(serializer.data)
