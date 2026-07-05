import uuid

from django.db import models
from django.contrib.auth.models import User

from documents.models import Document


class Comment(models.Model):
    """
    Threaded comments on a document.
    A comment can have replies using a self-referencing ForeignKey.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    content = models.TextField()

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="replies"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.author.username} - {self.content[:40]}"