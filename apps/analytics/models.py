from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.news.models import Article

User = settings.AUTH_USER_MODEL


class ArticleView(TimeStampedModel):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="views"
    )

    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["article", "created_at"]),
        ]

    def __str__(self):
        return f"View: {self.article_id}"
