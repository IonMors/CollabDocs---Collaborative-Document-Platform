from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):

    document_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag

        fields = [
            "id",
            "name",
            "document_count",
            "created_at",
        ]

    def get_document_count(self, obj):
        return obj.documents.count()