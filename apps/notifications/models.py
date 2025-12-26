from django.db import models
from django.conf import settings

from apps.core.models import TimeStampedModel, SoftDeleteModel
from apps.news.models import Article


class Notification(TimeStampedModel, SoftDeleteModel):
    class Type(models.TextChoices):
        BREAKING_NEWS = "BREAKING_NEWS", "Breaking News"
        COMMENT_REPLY = "COMMENT_REPLY", "Comment Reply"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    notification_type = models.CharField(
        max_length=50,
        choices=Type.choices
    )

    title = models.CharField(max_length=255)
    message = models.TextField()

    article = models.ForeignKey(
        Article,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["notification_type"]),
            models.Index(fields=["is_sent"]),
        ]

    def __str__(self):
        return f"{self.notification_type} → {self.user.email}"
