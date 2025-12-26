from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "notification_type",
        "is_sent",
        "created_at",
    )
    list_filter = ("notification_type", "is_sent")
    search_fields = ("title", "message", "user__email")
    ordering = ("-created_at",)
