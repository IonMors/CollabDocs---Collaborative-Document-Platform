import uuid

from django.db import models
from django.contrib.auth.models import User

from workspace.models import Workspace
from tags.models import Tag


class Document(models.Model):
    """
    A document belongs to a workspace.
    Each update creates a new DocumentVersion.
    """

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        REVIEW = "REVIEW", "Review"
        PUBLISHED = "PUBLISHED", "Published"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    title = models.CharField(max_length=255)

    content = models.TextField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_documents"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="documents",
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title


class DocumentVersion(models.Model):
    """
    Snapshot of a document.
    Created automatically whenever the document is created or updated.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="versions"
    )

    version_number = models.PositiveIntegerField()

    title = models.CharField(
        max_length=255
    )

    content = models.TextField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="document_versions"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-version_number"]

        unique_together = (
            "document",
            "version_number",
        )

    def __str__(self):
        return (
            f"{self.document.title} "
            f"(Version {self.version_number})"
        )