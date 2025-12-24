from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.news.models import Article

User = settings.AUTH_USER_MODEL


class Reaction(TimeStampedModel):
    class Type(models.TextChoices):
        LIKE = "like", "Like"
        BOOKMARK = "bookmark", "Bookmark"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reactions"
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="reactions"
    )
    type = models.CharField(
        max_length=20,
        choices=Type.choices
    )

    class Meta:
        unique_together = ("user", "article", "type")

    def __str__(self):
        return f"{self.user} {self.type} {self.article}"
