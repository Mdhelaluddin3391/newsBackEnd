from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "full_name",
        "role",
        "is_active",
        "is_staff",
        "created_at",
    )
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("email", "full_name")
    ordering = ("-created_at",)

    fieldsets = (
        ("Basic Info", {
            "fields": ("email", "full_name", "password")
        }),
        ("Role & Permissions", {
            "fields": ("role", "is_staff", "is_superuser")
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at", "last_login")
        }),
    )

    readonly_fields = ("created_at", "updated_at", "last_login")
