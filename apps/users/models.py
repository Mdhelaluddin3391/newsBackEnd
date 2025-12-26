from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
from django.utils import timezone

from apps.core.models import TimeStampedModel, SoftDeleteModel

import uuid
from django.utils import timezone
from datetime import timedelta
import uuid
from django.utils import timezone
from datetime import timedelta


class EmailVerificationToken(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="email_verification_tokens"
    )

    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expires_at = models.DateTimeField()
    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_token(cls, user, minutes=60):
        return cls.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(minutes=minutes)
        )

    def is_valid(self):
        return not self.verified and timezone.now() <= self.expires_at


class PasswordResetToken(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="password_reset_tokens"
    )

    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["token"]),
            models.Index(fields=["expires_at"]),
        ]

    @classmethod
    def create_token(cls, user, *, minutes=30):
        return cls.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(minutes=minutes)
        )

    def is_valid(self):
        return (not self.used) and timezone.now() <= self.expires_at

    def mark_used(self):
        self.used = True
        self.save(update_fields=["used"])





class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.SUPER_ADMIN)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel, SoftDeleteModel):
    class Role(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
        ADMIN = "ADMIN", "Admin"
        EDITOR = "EDITOR", "Editor / Journalist"
        AUTHOR = "AUTHOR", "Author / Reporter"
        MODERATOR = "MODERATOR", "Moderator"
        USER = "USER", "Normal User"

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["role"]),
        ]

    def __str__(self):
        return f"{self.email} ({self.role})"

    @property
    def is_admin(self):
        return self.role in {
            self.Role.SUPER_ADMIN,
            self.Role.ADMIN
        }

    @property
    def is_editor(self):
        return self.role == self.Role.EDITOR

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR
