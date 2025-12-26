from django.db import models
from django.conf import settings
from django.utils import timezone


class TimeStampedModel(models.Model):
    """
    Adds created_at and updated_at fields
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    Soft delete support for all models
    """
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    class Meta:
        abstract = True


class AuditLog(models.Model):
    """
    Tracks critical system actions
    """
    ACTION_CHOICES = (
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("APPROVE", "Approve"),
        ("LOGIN", "Login"),
        ("ROLE_CHANGE", "Role Change"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["model_name", "object_id"]),
            models.Index(fields=["action"]),
        ]

    def __str__(self):
        return f"{self.action} - {self.model_name} ({self.object_id})"




class BrandSettings(models.Model):
    """
    Singleton model for branding & email theming
    """
    brand_name = models.CharField(max_length=100, default="YourNews")
    primary_color = models.CharField(max_length=20, default="#0A58CA")
    secondary_color = models.CharField(max_length=20, default="#111111")

    logo = models.ImageField(
        upload_to="branding/",
        null=True,
        blank=True
    )

    support_email = models.EmailField(default="support@yournews.com")
    frontend_url = models.URLField(default="https://yournews.com")

    dark_mode_enabled = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Brand Settings"

    def __str__(self):
        return "Brand Settings"
