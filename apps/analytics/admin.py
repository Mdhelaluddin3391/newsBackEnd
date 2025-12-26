from django.contrib import admin
from .models import ArticleAnalytics, ArticleViewEvent


@admin.register(ArticleAnalytics)
class ArticleAnalyticsAdmin(admin.ModelAdmin):
    list_display = (
        "article",
        "total_views",
        "unique_users",
        "bounce_rate",
        "last_calculated_at",
    )
    ordering = ("-total_views",)
    readonly_fields = ("last_calculated_at",)


@admin.register(ArticleViewEvent)
class ArticleViewEventAdmin(admin.ModelAdmin):
    list_display = ("article", "user", "session_id", "created_at")
    search_fields = ("session_id", "user__email")
    ordering = ("-created_at",)
