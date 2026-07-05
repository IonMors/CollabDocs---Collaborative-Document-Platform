from django.db.models.signals import post_save
from django.dispatch import receiver

from audit.models import AuditLog
from .models import Document


@receiver(post_save, sender=Document)
def create_document_audit_log(sender, instance, created, **kwargs):
    """
    Automatically create an AuditLog whenever a Document
    is created or updated.
    """

    if created:
        action = AuditLog.Action.CREATED
    else:
        action = AuditLog.Action.UPDATED

    AuditLog.objects.create(
        actor=instance.created_by,
        action=action,
        model_name="Document",
        object_id=instance.id
    )