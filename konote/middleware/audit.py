"""Audit logging middleware — logs all state-changing requests."""
import json

from django.utils import timezone


# HTTP methods that change state
AUDITABLE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


class AuditMiddleware:
    """
    Automatically log state-changing HTTP requests to the audit database.
    Captures: user, action, path, IP address, timestamp.

    Detailed field-level changes are logged via model signals in the audit app.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only log state-changing requests from authenticated users
        if (
            request.method in AUDITABLE_METHODS
            and hasattr(request, "user")
            and request.user.is_authenticated
            and response.status_code < 400  # Only successful requests
        ):
            self._log_request(request, response)

        return response

    def _log_request(self, request, response):
        """Write an audit log entry."""
        try:
            from apps.audit.models import AuditLog

            AuditLog.objects.using("audit").create(
                event_timestamp=timezone.now(),
                user_id=request.user.id,
                user_display=request.user.get_display_name(),
                ip_address=self._get_client_ip(request),
                action=request.method.lower(),
                resource_type=self._extract_resource_type(request.path),
                resource_id=self._extract_resource_id(request.path),
                metadata={
                    "path": request.path,
                    "status_code": response.status_code,
                },
            )
        except Exception:
            # Audit logging should never break the application
            pass

    def _get_client_ip(self, request):
        """Get client IP, respecting X-Forwarded-For from reverse proxy."""
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")

    def _extract_resource_type(self, path):
        """Extract resource type from URL path (e.g., /clients/5/ -> client)."""
        parts = [p for p in path.strip("/").split("/") if p]
        return parts[0] if parts else "unknown"

    def _extract_resource_id(self, path):
        """Extract numeric resource ID from URL path if present."""
        parts = path.strip("/").split("/")
        for part in parts:
            if part.isdigit():
                return int(part)
        return None
