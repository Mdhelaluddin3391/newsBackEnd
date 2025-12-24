from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

User = settings.AUTH_USER_MODEL


class Notification(TimeStampedModel):
    class Type(models.TextChoices):
        SYSTEM = "system", "System"
        NEWS = "news", "News"
        COMMENT = "comment", "Comment"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(max_length=255)
    message = models.TextField()

    type = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.SYSTEM
    )

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification({self.user}, {self.title})"


class NotificationPreference(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="notification_pref"
    )

    email_enabled = models.BooleanField(default=True)
    in_app_enabled = models.BooleanField(default=True)
    push_enabled = models.BooleanField(default=False)  # future

    def __str__(self):
        return f"Preferences({self.user})"
