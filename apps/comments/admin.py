from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "article", "parent", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("content",)
