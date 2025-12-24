from rest_framework import serializers
from .models import Category, Article


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    category = CategorySerializer()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "summary",
            "content",
            "author",
            "category",
            "status",
            "published_at",
            "created_at",
        ]


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["title", "slug", "summary", "content", "category"]
