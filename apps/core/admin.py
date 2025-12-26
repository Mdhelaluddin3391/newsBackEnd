from django.contrib import admin
from .models import BrandSettings


@admin.register(BrandSettings)
class BrandSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not BrandSettings.objects.exists()
