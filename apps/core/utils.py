from .models import AuditLog


def create_audit_log(
    *,
    user=None,
    action,
    model_name,
    object_id,
    description="",
    ip_address=None
):
    AuditLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=str(object_id),
        description=description,
        ip_address=ip_address,
    )
