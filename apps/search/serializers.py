from rest_framework import serializers
from apps.news.models import Article


class SearchArticleSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "summary",
            "category",
            "author",
            "published_at",
        ]
