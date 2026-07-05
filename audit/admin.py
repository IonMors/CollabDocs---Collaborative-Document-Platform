from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        "actor",
        "action",
        "model_name",
        "timestamp",
    )

    list_filter = (
        "action",
        "model_name",
    )

    search_fields = (
        "model_name",
    )