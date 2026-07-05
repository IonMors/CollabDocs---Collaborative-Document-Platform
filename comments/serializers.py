from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):

    author_username = serializers.CharField(
        source="author.username",
        read_only=True
    )

    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment

        fields = [
            "id",
            "document",
            "author",
            "author_username",
            "content",
            "parent",
            "replies",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "author",
            "replies",
        )

    def get_replies(self, obj):
        """
        Return direct replies to this comment.
        """

        replies = obj.replies.all()

        return CommentSerializer(
            replies,
            many=True
        ).data

    def validate_content(self, value):

        value = value.strip()

        if len(value) == 0:
            raise serializers.ValidationError(
                "Comment cannot be empty."
            )

        return value


class ReplySerializer(serializers.Serializer):

    content = serializers.CharField()

    def validate_content(self, value):

        value = value.strip()

        if len(value) == 0:
            raise serializers.ValidationError(
                "Reply cannot be empty."
            )

        return value