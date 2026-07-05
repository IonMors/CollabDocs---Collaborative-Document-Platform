from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API for Audit Logs.
    """

    serializer_class = AuditLogSerializer

    permission_classes = [
        IsAuthenticated
    ]

    queryset = (
        AuditLog.objects
        .select_related("actor")
        .all()
    )