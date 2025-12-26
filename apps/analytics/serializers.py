from rest_framework import serializers
from .models import ArticleAnalytics


class ArticleAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleAnalytics
        fields = (
            "total_views",
            "unique_users",
            "total_read_time",
            "bounce_rate",
            "last_calculated_at",
        )
