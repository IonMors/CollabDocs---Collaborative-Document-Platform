from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Workspace, WorkspaceMember


class WorkspaceMemberSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = WorkspaceMember

        fields = [
            "id",
            "user",
            "username",
            "role",
            "joined_at",
        ]


class WorkspaceSerializer(serializers.ModelSerializer):

    owner_username = serializers.CharField(
        source="owner.username",
        read_only=True
    )

    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Workspace

        fields = [
            "id",
            "name",
            "description",
            "owner",
            "owner_username",
            "is_active",
            "member_count",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "owner",
            "member_count",
        )

    def get_member_count(self, obj):
        return obj.members.count()

    def validate_name(self, value):

        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Workspace name must be at least 3 characters."
            )

        return value


class InviteMemberSerializer(serializers.Serializer):

    user_id = serializers.IntegerField()

    role = serializers.ChoiceField(
        choices=WorkspaceMember.Role.choices
    )