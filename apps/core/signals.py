from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import AuditLog
from .utils import create_audit_log


@receiver(post_save)
def audit_on_save(sender, instance, created, **kwargs):
    if sender._meta.app_label not in {"users", "news", "comments"}:
        return

    action = "CREATE" if created else "UPDATE"
    create_audit_log(
        action=action,
        model_name=sender.__name__,
        object_id=instance.pk,
        description=f"{sender.__name__} {action.lower()}",
    )


@receiver(post_delete)
def audit_on_delete(sender, instance, **kwargs):
    if sender._meta.app_label not in {"users", "news", "comments"}:
        return

    create_audit_log(
        action="DELETE",
        model_name=sender.__name__,
        object_id=instance.pk,
        description=f"{sender.__name__} deleted",
    )
