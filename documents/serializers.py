from rest_framework import serializers

from .models import Document, DocumentVersion


class DocumentVersionSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(
        source="created_by.username",
        read_only=True
    )

    class Meta:
        model = DocumentVersion
        fields = [
            "id",
            "document",
            "version_number",
            "title",
            "content",
            "created_by",
            "created_at",
        ]


class DocumentSerializer(serializers.ModelSerializer):

    workspace_name = serializers.CharField(
        source="workspace.name",
        read_only=True
    )

    created_by_username = serializers.CharField(
        source="created_by.username",
        read_only=True
    )

    version_count = serializers.SerializerMethodField()

    class Meta:
        model = Document

        fields = [
            "id",
            "workspace",
            "workspace_name",
            "title",
            "content",
            "status",
            "tags",
            "created_by",
            "created_by_username",
            "version_count",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "created_by",
            "version_count",
        ]

    # -----------------------------------------
    # SerializerMethodField
    # -----------------------------------------
    def get_version_count(self, obj):
        return obj.versions.count()

    # -----------------------------------------
    # Custom Validation
    # -----------------------------------------
    def validate_title(self, value):

        value = value.strip()

        if len(value) < 5:
            raise serializers.ValidationError(
                "Document title must be at least 5 characters."
            )

        return value