from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Comment
from .serializers import (
    CommentSerializer,
    ReplySerializer,
)


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    queryset = (
        Comment.objects
        .select_related(
            "author",
            "document",
            "parent",
        )
    )

    # -------------------------------------
    # CREATE COMMENT
    # -------------------------------------
    def perform_create(self, serializer):

        serializer.save(
            author=self.request.user
        )

    # -------------------------------------
    # REPLY TO COMMENT
    # POST /comments/{id}/reply/
    # -------------------------------------
    @action(
        detail=True,
        methods=["post"],
    )
    def reply(self, request, pk=None):

        parent_comment = self.get_object()

        serializer = ReplySerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        reply = Comment.objects.create(
            document=parent_comment.document,
            author=request.user,
            parent=parent_comment,
            content=serializer.validated_data["content"],
        )

        return Response(
            CommentSerializer(reply).data,
            status=status.HTTP_201_CREATED,
        )