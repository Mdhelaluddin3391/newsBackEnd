from django.db import models
from django.conf import settings
from django.utils import timezone
from ckeditor.fields import RichTextField

from apps.core.models import TimeStampedModel, SoftDeleteModel

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Article(models.Model):

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("review", "In Review"),
        ("approved", "Approved"),
        ("published", "Published"),
        ("archived", "Archived"),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    content = models.TextField()  # HTML allowed
    thumbnail = models.ImageField(upload_to="articles/", blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    views = models.PositiveIntegerField(default=0)
    read_time = models.PositiveIntegerField(default=5)

    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title



class ArticleTranslation(TimeStampedModel, SoftDeleteModel):
    """
    Placeholder for future translations
    (Reader language change support)
    """

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="translations"
    )

    language = models.CharField(max_length=10)
    title = models.CharField(max_length=300)
    summary = models.TextField()
    content = models.TextField()

    class Meta:
        unique_together = ("article", "language")
        indexes = [
            models.Index(fields=["language"]),
        ]

    def __str__(self):
        return f"{self.article.title} ({self.language})"
