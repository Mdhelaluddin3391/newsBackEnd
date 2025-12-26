from django.core.mail import send_mail
from django.conf import settings
from .models import Notification, NotificationPreference

def get_or_create_preferences(user):
    pref, _ = NotificationPreference.objects.get_or_create(user=user)
    return pref

def notify(*, user, title, message, type="system", send_email=False):
    """
    Backend mein notification bhejone ka main function.
    """
    pref = get_or_create_preferences(user)

    # In-App Notification check
    if pref.in_app_enabled:
        Notification.objects.create(
            user=user,
            title=title,
            message=message,
            type=type,
        )

    # Email Notification check
    if send_email and pref.email_enabled and user.email:
        send_mail(
            subject=title,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )