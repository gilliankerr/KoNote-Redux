"""PDF export views for client progress reports and funder reports."""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone

from apps.clients.models import ClientProgramEnrolment
from apps.events.models import Event
from apps.notes.models import MetricValue, ProgressNote
from apps.plans.models import PlanSection, PlanTarget, PlanTargetMetric

from .pdf_utils import audit_pdf_export, render_pdf
from .views import _get_client_or_403


@login_required
def client_progress_pdf(request, client_id):
    """Generate a PDF progress report for an individual client."""
    client = _get_client_or_403(request, client_id)
    if client is None:
        return HttpResponseForbidden("You do not have access to this client.")

    # Programme enrolments
    enrolments = ClientProgramEnrolment.objects.filter(
        client_file=client, status="enrolled"
    ).select_related("program")

    # Plan sections and targets
    sections = PlanSection.objects.filter(
        client_file=client, status="default"
    ).prefetch_related("targets")

    # Build metric tables: for each target, collect metric values
    metric_tables = []
    targets = PlanTarget.objects.filter(
        client_file=client, status="default"
    ).prefetch_related("metrics")

    for target in targets:
        ptm_links = PlanTargetMetric.objects.filter(
            plan_target=target
        ).select_related("metric_def")

        for ptm in ptm_links:
            metric_def = ptm.metric_def
            values = MetricValue.objects.filter(
                metric_def=metric_def,
                progress_note_target__plan_target=target,
                progress_note_target__progress_note__client_file=client,
                progress_note_target__progress_note__status="default",
            ).select_related(
                "progress_note_target__progress_note__author"
            ).order_by(
                "progress_note_target__progress_note__created_at"
            )

            if not values:
                continue

            rows = []
            for mv in values:
                note = mv.progress_note_target.progress_note
                try:
                    numeric_val = float(mv.value)
                except (ValueError, TypeError):
                    numeric_val = mv.value
                rows.append({
                    "date": note.effective_date.strftime("%Y-%m-%d"),
                    "value": numeric_val,
                    "author": note.author.display_name,
                })

            metric_tables.append({
                "target_name": target.name,
                "metric_name": metric_def.name,
                "unit": metric_def.unit or "",
                "min_value": metric_def.min_value,
                "max_value": metric_def.max_value,
                "rows": rows,
            })

    # Recent progress notes (last 20)
    notes = ProgressNote.objects.filter(
        client_file=client, status="default"
    ).select_related("author")[:20]

    # Recent events (last 20)
    events = Event.objects.filter(
        client_file=client, status="default"
    ).select_related("event_type")[:20]

    context = {
        "client": client,
        "enrolments": enrolments,
        "sections": sections,
        "metric_tables": metric_tables,
        "notes": notes,
        "events": events,
        "generated_at": timezone.now(),
        "generated_by": request.user.display_name,
    }

    filename = f"progress_report_{client.record_id or client.pk}_{timezone.now():%Y-%m-%d}.pdf"

    audit_pdf_export(request, "export", "client_progress_pdf", {
        "client_id": client.pk,
        "record_id": client.record_id,
        "format": "pdf",
    })

    return render_pdf("reports/pdf_client_progress.html", context, filename)


def generate_funder_pdf(request, program, selected_metrics, date_from, date_to, rows, unique_clients):
    """Generate a PDF funder report. Called from export_form view."""
    context = {
        "program": program,
        "metrics": selected_metrics,
        "date_from": date_from,
        "date_to": date_to,
        "rows": rows,
        "total_clients": len(unique_clients),
        "total_data_points": len(rows),
        "generated_at": timezone.now(),
        "generated_by": request.user.display_name,
    }

    filename = f"funder_report_{program.name.replace(' ', '_')}_{date_from}_{date_to}.pdf"

    audit_pdf_export(request, "export", "funder_report_pdf", {
        "program": program.name,
        "metrics": [m.name for m in selected_metrics],
        "date_from": str(date_from),
        "date_to": str(date_to),
        "total_clients": len(unique_clients),
        "total_data_points": len(rows),
        "format": "pdf",
    })

    return render_pdf("reports/pdf_funder_report.html", context, filename)
