from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Tag
from .serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):

    serializer_class = TagSerializer

    permission_classes = [IsAuthenticated]

    queryset = Tag.objects.all()

    # ------------------------------------------
    # GET DOCUMENT IDS FOR A TAG
    # GET /tags/{id}/documents/
    # ------------------------------------------
    @action(
        detail=True,
        methods=["get"]
    )
    def documents(self, request, pk=None):

        tag = self.get_object()

        document_ids = tag.documents.values_list(
            "id",
            flat=True
        )

        return Response(
            {
                "tag": tag.name,
                "documents": list(document_ids)
            },
            status=status.HTTP_200_OK
        )