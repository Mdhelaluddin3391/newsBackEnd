from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from apps.core.models import TimeStampedModel, SoftDeleteModel
from apps.news.models import Article


BAD_WORDS = [
    "abuse",
    "badword",
    "spam",
]


def contains_bad_words(text: str) -> bool:
    text = text.lower()
    return any(word in text for word in BAD_WORDS)


class Comment(TimeStampedModel, SoftDeleteModel):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    content = models.TextField()

    edit_count = models.PositiveSmallIntegerField(default=0)
    is_reported = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["article"]),
            models.Index(fields=["user"]),
            models.Index(fields=["is_reported"]),
        ]

    def clean(self):
        # Bad word filter
        if contains_bad_words(self.content):
            raise ValidationError("Comment contains inappropriate language")

        # Depth check (max 3)
        depth = 1
        parent = self.parent
        while parent:
            depth += 1
            if depth > 3:
                raise ValidationError("Maximum comment depth exceeded")
            parent = parent.parent

    def can_edit(self):
        return self.edit_count < 2

    def edit(self, new_content: str):
        if not self.can_edit():
            raise ValidationError("Edit limit exceeded")

        if contains_bad_words(new_content):
            raise ValidationError("Comment contains inappropriate language")

        self.content = new_content
        self.edit_count += 1
        self.save(update_fields=["content", "edit_count", "updated_at"])

    def report(self):
        self.is_reported = True
        self.save(update_fields=["is_reported"])

    def __str__(self):
        return f"Comment by {self.user.email}"
