from rest_framework import serializers
from .models import SearchIndex


class SearchResultSerializer(serializers.ModelSerializer):
    article_id = serializers.IntegerField(source="article.id")
    slug = serializers.CharField(source="article.slug")

    class Meta:
        model = SearchIndex
        fields = (
            "article_id",
            "slug",
            "title",
            "summary",
            "category",
            "article_type",
            "published_at",
        )
