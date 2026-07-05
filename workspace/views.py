from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.db.models import Count

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Workspace, WorkspaceMember
from .serializers import (
    WorkspaceSerializer,
    WorkspaceMemberSerializer,
    InviteMemberSerializer,
)


class WorkspaceViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Workspace.
    """

    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]

    queryset = (
        Workspace.objects
        .select_related("owner")
        .annotate(member_total=Count("members"))
    )

    # ---------------------------------------------------------
    # CREATE WORKSPACE
    # Owner is automatically added as ADMIN.
    # Everything happens inside one transaction.
    # ---------------------------------------------------------
    def perform_create(self, serializer):

        with transaction.atomic():

            workspace = serializer.save(
                owner=self.request.user
            )

            WorkspaceMember.objects.create(
                workspace=workspace,
                user=self.request.user,
                role=WorkspaceMember.Role.ADMIN
            )

    # ---------------------------------------------------------
    # INVITE MEMBER
    # POST /workspaces/{id}/invite/
    # ---------------------------------------------------------
    @action(
        detail=True,
        methods=["post"]
    )
    def invite(self, request, pk=None):

        workspace = self.get_object()

        serializer = InviteMemberSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            user = User.objects.get(
                pk=serializer.validated_data["user_id"]
            )

        except User.DoesNotExist:

            return Response(
                {
                    "message": "User not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            member = WorkspaceMember.objects.create(
                workspace=workspace,
                user=user,
                role=serializer.validated_data["role"]
            )

        except IntegrityError:

            return Response(
                {
                    "message":
                        "User is already a member of this workspace."
                },
                status=status.HTTP_409_CONFLICT
            )

        return Response(
            WorkspaceMemberSerializer(member).data,
            status=status.HTTP_201_CREATED
        )

    # ---------------------------------------------------------
    # GET MEMBERS
    # GET /workspaces/{id}/members/
    # ---------------------------------------------------------
    @action(
        detail=True,
        methods=["get"]
    )
    def members(self, request, pk=None):

        workspace = self.get_object()

        members = (
            workspace.members
            .select_related("user")
            .all()
        )

        serializer = WorkspaceMemberSerializer(
            members,
            many=True
        )

        return Response(serializer.data)

    # ---------------------------------------------------------
    # WORKSPACE STATS
    # GET /workspaces/{id}/stats/
    # ---------------------------------------------------------
    @action(
        detail=True,
        methods=["get"]
    )
    def stats(self, request, pk=None):

        workspace = (
            Workspace.objects
            .annotate(
                total_members=Count("members"),
                total_documents=Count(
                    "documents",
                    distinct=True
                )
            )
            .get(pk=pk)
        )

        return Response({
            "workspace": workspace.name,
            "members": workspace.total_members,
            "documents": workspace.total_documents,
        })