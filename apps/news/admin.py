from django.contrib import admin
from .models import Article, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "is_active")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "category", "published_at")
    list_filter = ("status", "category")
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        ("Basic", {
            "fields": ("title", "slug", "summary", "content", "thumbnail")
        }),
        ("Meta", {
            "fields": ("category", "author", "status", "published_at")
        }),
        ("Stats", {
            "fields": ("views", "read_time")
        }),
    )
