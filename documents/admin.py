from django.contrib import admin

from .models import Document, DocumentVersion


class DocumentVersionInline(admin.TabularInline):
    model = DocumentVersion
    extra = 0
    readonly_fields = (
        "version_number",
        "created_by",
        "created_at",
    )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "workspace",
        "status",
        "created_by",
        "updated_at",
    )

    list_filter = (
        "status",
        "workspace",
    )

    search_fields = (
        "title",
        "content",
    )

    filter_horizontal = (
        "tags",
    )

    inlines = [
        DocumentVersionInline,
    ]


@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):

    list_display = (
        "document",
        "version_number",
        "created_by",
        "created_at",
    )

    search_fields = (
        "document__title",
    )

    list_filter = (
        "created_at",
    )