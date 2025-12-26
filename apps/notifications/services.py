from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from .models import Notification

from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.conf import settings


def send_html_email(
    *,
    subject,
    to_email,
    template_name,
    context,
):
    brand = BrandSettings.objects.first()

    html_content = render_to_string(
        template_name,
        {
            **context,
            "brand": brand,
            "dark_mode": brand.dark_mode_enabled if brand else False,
            "year": now().year,
        }
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)


def send_password_reset_email(*, email, reset_link):
    send_mail(
        subject="Reset your password",
        message=f"Reset your password using this link:\n{reset_link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=True,
    )



def send_email_notification(notification: Notification):
    send_mail(
        subject=notification.title,
        message=notification.message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[notification.user.email],
        fail_silently=True,
    )

    notification.is_sent = True
    notification.sent_at = timezone.now()
    notification.save(update_fields=["is_sent", "sent_at"])
