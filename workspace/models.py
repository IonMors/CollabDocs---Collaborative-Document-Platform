import uuid

from django.db import models
from django.contrib.auth.models import User


class Workspace(models.Model):
    """
    A collaborative workspace.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(max_length=255)

    description = models.TextField(
        blank=True,
        null=True
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_workspaces"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class WorkspaceMember(models.Model):
    """
    Users belonging to a workspace.
    """

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        EDITOR = "EDITOR", "Editor"
        VIEWER = "VIEWER", "Viewer"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="members"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="workspace_memberships"
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VIEWER
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["joined_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "user"],
                name="unique_workspace_member"
            )
        ]

    def __str__(self):
        return f"{self.user.username} ({self.role}) - {self.workspace.name}"