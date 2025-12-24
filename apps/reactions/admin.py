from django.contrib import admin
from .models import Reaction


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ("user", "article", "type", "created_at")
    list_filter = ("type",)
