from rest_framework import serializers
from apps.news.models import Article


class AnalyticsArticleSerializer(serializers.ModelSerializer):
    view_count = serializers.IntegerField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "view_count",
            "published_at",
        ]
