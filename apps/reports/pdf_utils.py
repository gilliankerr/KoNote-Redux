"""PDF generation utilities using WeasyPrint."""
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils import timezone
from weasyprint import HTML

from apps.audit.models import AuditLog


def render_pdf(template_name, context, filename="report.pdf"):
    """Render a Django template to a PDF HttpResponse."""
    html_string = render_to_string(template_name, context)
    # Use STATIC_ROOT as base_url so WeasyPrint can resolve {% static %} paths
    base_url = getattr(settings, "STATIC_ROOT", None) or "."
    pdf_bytes = HTML(string=html_string, base_url=base_url).write_pdf()
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def audit_pdf_export(request, action, resource_type, metadata):
    """Create an audit log entry for a PDF export."""
    AuditLog.objects.using("audit").create(
        event_timestamp=timezone.now(),
        user_id=request.user.pk,
        user_display=request.user.display_name,
        action=action,
        resource_type=resource_type,
        metadata=metadata,
    )
