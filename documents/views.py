from django.db import transaction
from django.db.models import Count, Q

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Document, DocumentVersion
from .serializers import (
    DocumentSerializer,
    DocumentVersionSerializer,
)


class DocumentViewSet(viewsets.ModelViewSet):

    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    queryset = (
        Document.objects
        .select_related(
            "workspace",
            "created_by",
        )
        .prefetch_related(
            "tags",
        )
    )

    # -------------------------------------------------
    # FILTERING
    # -------------------------------------------------
    def get_queryset(self):

        queryset = super().get_queryset()

        search = self.request.query_params.get("search")
        status_filter = self.request.query_params.get("status")
        workspace = self.request.query_params.get("workspace")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            )

        if status_filter:
            queryset = queryset.filter(
                status=status_filter
            )

        if workspace:
            queryset = queryset.filter(
                workspace=workspace
            )

        return queryset

    # -------------------------------------------------
    # CREATE DOCUMENT
    # -------------------------------------------------
    def perform_create(self, serializer):

        with transaction.atomic():

            document = serializer.save(
                created_by=self.request.user
            )

            version_number = (
                document.versions.count() + 1
            )

            DocumentVersion.objects.create(
                document=document,
                version_number=version_number,
                title=document.title,
                content=document.content,
                created_by=self.request.user,
            )

    # -------------------------------------------------
    # UPDATE DOCUMENT
    # -------------------------------------------------
    def perform_update(self, serializer):

        with transaction.atomic():

            document = serializer.save()

            version_number = (
                document.versions.count() + 1
            )

            DocumentVersion.objects.create(
                document=document,
                version_number=version_number,
                title=document.title,
                content=document.content,
                created_by=self.request.user,
            )

    # -------------------------------------------------
    # GET DOCUMENT VERSIONS
    # -------------------------------------------------
    @action(
        detail=True,
        methods=["get"],
    )
    def versions(self, request, pk=None):

        document = self.get_object()

        versions = (
            document.versions.all()
        )

        serializer = DocumentVersionSerializer(
            versions,
            many=True
        )

        return Response(serializer.data)

    # -------------------------------------------------
    # DOCUMENT SUMMARY
    # -------------------------------------------------
    @action(
        detail=False,
        methods=["get"],
    )
    def summary(self, request):

        total_documents = (
            Document.objects.count()
        )

        total_versions = (
            DocumentVersion.objects.count()
        )

        draft_documents = (
            Document.objects.filter(
                status=Document.Status.DRAFT
            ).count()
        )

        review_documents = (
            Document.objects.filter(
                status=Document.Status.REVIEW
            ).count()
        )

        published_documents = (
            Document.objects.filter(
                status=Document.Status.PUBLISHED
            ).count()
        )

        return Response({

            "total_documents": total_documents,

            "total_versions": total_versions,

            "draft_documents": draft_documents,

            "review_documents": review_documents,

            "published_documents": published_documents,

        })
