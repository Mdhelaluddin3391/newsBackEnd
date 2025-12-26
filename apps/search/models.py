from django.db import models
from apps.core.models import TimeStampedModel, SoftDeleteModel
from apps.news.models import Article


class SearchIndex(TimeStampedModel, SoftDeleteModel):
    """
    DB mirror of indexed content (fallback + debugging)
    """
    article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        related_name="search_index"
    )

    title = models.TextField()
    summary = models.TextField()
    content = models.TextField()

    category = models.CharField(max_length=100)
    article_type = models.CharField(max_length=50)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["article_type"]),
            models.Index(fields=["published_at"]),
        ]

    def __str__(self):
        return f"SearchIndex → {self.article.title}"
