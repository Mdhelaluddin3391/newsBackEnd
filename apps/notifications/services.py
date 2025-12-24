from django.core.mail import send_mail
from django.conf import settings

from .models import Notification, NotificationPreference


def get_or_create_preferences(user):
    pref, _ = NotificationPreference.objects.get_or_create(user=user)
    return pref


def send_in_app_notification(user, title, message, type="system"):
    pref = get_or_create_preferences(user)

    if not pref.in_app_enabled:
        return None

    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        type=type,
    )


def send_email_notification(user, subject, message):
    pref = get_or_create_preferences(user)

    if not pref.email_enabled or not user.email:
        return

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )


def notify(
    *,
    user,
    title,
    message,
    type="system",
    send_email=False,
):
    """
    Single entry-point for notifications
    """
    send_in_app_notification(user, title, message, type)

    if send_email:
        send_email_notification(user, title, message)
