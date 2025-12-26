from django.contrib import admin
from .models import SearchIndex


@admin.register(SearchIndex)
class SearchIndexAdmin(admin.ModelAdmin):
    list_display = (
        "article",
        "category",
        "article_type",
        "published_at",
    )
    search_fields = ("title", "summary", "content")
    ordering = ("-published_at",)
