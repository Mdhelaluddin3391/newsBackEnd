from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "article",
        "parent",
        "edit_count",
        "is_reported",
        "created_at",
    )
    list_filter = ("is_reported", "created_at")
    search_fields = ("content", "user__email")
    ordering = ("-created_at",)

    readonly_fields = ("edit_count",)
