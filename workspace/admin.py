from django.contrib import admin

from .models import Workspace, WorkspaceMember


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "owner__username",
    )

    list_filter = (
        "is_active",
    )


@admin.register(WorkspaceMember)
class WorkspaceMemberAdmin(admin.ModelAdmin):
    list_display = (
        "workspace",
        "user",
        "role",
        "joined_at",
    )

    search_fields = (
        "workspace__name",
        "user__username",
    )

    list_filter = (
        "role",
    )