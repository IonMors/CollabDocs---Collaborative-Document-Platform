import uuid

from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):
    """
    Stores audit events for important actions.
    """

    class Action(models.TextChoices):
        CREATED = "CREATED", "Created"
        UPDATED = "UPDATED", "Updated"
        DELETED = "DELETED", "Deleted"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="audit_logs"
    )

    action = models.CharField(
        max_length=20,
        choices=Action.choices
    )

    model_name = models.CharField(
        max_length=100
    )

    object_id = models.UUIDField()

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return (
            f"{self.actor} - "
            f"{self.action} - "
            f"{self.model_name}"
        )