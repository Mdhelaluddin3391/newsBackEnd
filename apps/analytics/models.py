from django.db import models
from django.conf import settings

from apps.core.models import TimeStampedModel, SoftDeleteModel
from apps.news.models import Article


class ArticleViewEvent(TimeStampedModel):
    """
    Append-only event table for views (high write volume safe)
    """
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="view_events"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    session_id = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["article"]),
            models.Index(fields=["session_id"]),
            models.Index(fields=["created_at"]),
        ]


class ArticleAnalytics(TimeStampedModel, SoftDeleteModel):
    """
    Aggregated analytics (read-optimized)
    """
    article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        related_name="analytics"
    )

    total_views = models.PositiveIntegerField(default=0)
    unique_users = models.PositiveIntegerField(default=0)

    total_read_time = models.PositiveIntegerField(
        default=0,
        help_text="Seconds"
    )

    bounce_rate = models.FloatField(
        default=0.0,
        help_text="Percentage"
    )

    last_calculated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["total_views"]),
            models.Index(fields=["unique_users"]),
        ]

    def __str__(self):
        return f"Analytics for {self.article.title}"
