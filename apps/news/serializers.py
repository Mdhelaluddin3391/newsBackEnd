from rest_framework import serializers
from .models import Article, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source="author.full_name",
        read_only=True
    )

    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "slug",
            "summary",
            "content",
            "article_type",
            "status",
            "category",
            "author_name",
            "published_at",
            "thumbnail",
            "language",
        )
        read_only_fields = (
            "status",
            "published_at",
            "author_name",
        )
