"""Client data erasure service — the core deletion logic.

This module contains the business logic for the multi-PM erasure approval
workflow. Views call these functions; they never call client.delete() directly.
"""
import logging

from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


def build_data_summary(client_file):
    """Count all related records for a ClientFile.

    Returns a dict of integer counts only. Must never include PII.
    Used to populate ErasureRequest.data_summary at request time.
    """
    from apps.events.models import Alert, Event
    from apps.notes.models import MetricValue, ProgressNote
    from apps.plans.models import PlanSection, PlanTarget

    from .models import ClientDetailValue, ClientProgramEnrolment

    return {
        "progress_notes": ProgressNote.objects.filter(client_file=client_file).count(),
        "plan_sections": PlanSection.objects.filter(client_file=client_file).count(),
        "plan_targets": PlanTarget.objects.filter(client_file=client_file).count(),
        "events": Event.objects.filter(client_file=client_file).count(),
        "alerts": Alert.objects.filter(client_file=client_file).count(),
        "custom_field_values": ClientDetailValue.objects.filter(client_file=client_file).count(),
        "enrolments": ClientProgramEnrolment.objects.filter(client_file=client_file).count(),
        "metric_values": MetricValue.objects.filter(
            progress_note_target__progress_note__client_file=client_file
        ).count(),
    }


def get_required_programs(client_file):
    """Return list of programs that need PM approval for this client.

    Logic (never returns empty):
    1. Active enrolments (status="enrolled")
    2. If empty: historical enrolments (any status)
    3. If still empty: all active programs (any PM can approve)
    """
    from apps.programs.models import Program

    from .models import ClientProgramEnrolment

    # 1. Active enrolments
    active_program_ids = list(
        ClientProgramEnrolment.objects.filter(
            client_file=client_file, status="enrolled",
        ).values_list("program_id", flat=True).distinct()
    )
    if active_program_ids:
        return list(Program.objects.filter(pk__in=active_program_ids, status="active").values_list("pk", flat=True))

    # 2. Historical enrolments (includes unenrolled)
    historical_program_ids = list(
        ClientProgramEnrolment.objects.filter(
            client_file=client_file,
        ).values_list("program_id", flat=True).distinct()
    )
    if historical_program_ids:
        active_programs = list(
            Program.objects.filter(pk__in=historical_program_ids, status="active").values_list("pk", flat=True)
        )
        if active_programs:
            return active_programs

    # 3. Safety net: any active program (so at least one PM must approve)
    any_program = Program.objects.filter(status="active").values_list("pk", flat=True).first()
    if any_program:
        return [any_program]

    # Should never happen — there must be at least one program in the system
    raise ValueError("Cannot determine approval requirements: no active programs exist.")


def check_all_approved(erasure_request):
    """Check whether all required programs have an approval.

    Uses count-based comparison to handle edge case of deleted programs.
    """
    required_count = len(erasure_request.programs_required)
    approval_count = erasure_request.approvals.count()
    return approval_count >= required_count


def is_deadlocked(erasure_request):
    """Check if the requester is the only active PM for all remaining unapproved programs.

    Returns True if an admin fallback is needed to break the deadlock.
    """
    from apps.programs.models import UserProgramRole

    if erasure_request.status != "pending":
        return False

    requester = erasure_request.requested_by
    if requester is None:
        return False

    # Find programs that still need approval
    approved_program_ids = set(
        erasure_request.approvals.values_list("program_id", flat=True)
    )
    remaining_program_ids = [
        pk for pk in erasure_request.programs_required
        if pk not in approved_program_ids
    ]

    if not remaining_program_ids:
        return False  # All approved, not deadlocked

    # For each remaining program, check if there's an active PM who isn't the requester
    for program_id in remaining_program_ids:
        other_pms = UserProgramRole.objects.filter(
            program_id=program_id,
            role="program_manager",
            status="active",
        ).exclude(user=requester)
        if other_pms.exists():
            return False  # At least one other PM can approve this program

    return True  # Requester is the only PM for all remaining programs


def record_approval(erasure_request, user, program, ip_address, review_notes=""):
    """Record a PM's approval for one program and auto-execute if all approved.

    Uses select_for_update() to prevent concurrent double-execution.

    Returns:
        tuple: (approval, executed) — the ErasureApproval and whether erasure ran.

    Raises:
        ValueError: If request isn't pending, user can't approve, etc.
    """
    from .models import ErasureApproval

    with transaction.atomic():
        # Lock the request row to prevent concurrent double-execution
        er = type(erasure_request).objects.select_for_update().get(pk=erasure_request.pk)

        if er.status != "pending":
            raise ValueError(f"Cannot approve — status is '{er.status}', not 'pending'.")

        if er.requested_by == user and not _is_admin_fallback(er, user):
            raise ValueError(_("You cannot approve your own erasure request."))

        # Check this program hasn't already been approved
        if er.approvals.filter(program=program).exists():
            raise ValueError(f"Program '{program.name}' has already been approved.")

        # Create the approval record
        approval = ErasureApproval.objects.create(
            erasure_request=er,
            program=program,
            approved_by=user,
            approved_by_display=user.get_display_name(),
            review_notes=review_notes,
        )

        # Log the individual approval
        _log_audit(
            user=user,
            action="update",
            resource_type="erasure_approval",
            resource_id=er.pk,
            ip_address=ip_address,
            metadata={
                "client_pk": er.client_pk,
                "program_id": program.pk,
                "program_name": program.name,
                "approval_id": approval.pk,
            },
        )

        # Check if all programs are now approved
        if check_all_approved(er):
            execute_erasure(er, ip_address)
            return approval, True

    return approval, False


def execute_erasure(erasure_request, ip_address):
    """Execute the actual client data deletion. Called internally only.

    Must be called within a transaction (record_approval wraps it).

    1. Scrub PII on linked RegistrationSubmissions
    2. Set ClientFile convenience flags
    3. Delete the ClientFile (CASCADE handles all related records)
    4. Update ErasureRequest status
    5. Create audit log entry (outside main transaction since audit DB is separate)
    """
    from apps.registration.models import RegistrationSubmission

    client = erasure_request.client_file
    if client is None:
        raise ValueError("Client file no longer exists.")

    client_pk = client.pk
    record_id = client.record_id

    # 1. Scrub PII on linked RegistrationSubmissions (before delete nulls the FK)
    RegistrationSubmission.objects.filter(client_file=client).update(
        _first_name_encrypted=b"",
        _last_name_encrypted=b"",
        _email_encrypted=b"",
        _phone_encrypted=b"",
        email_hash="",
    )

    # 2. Delete the ClientFile — CASCADE handles all related records
    client.delete()

    # 3. Update the ErasureRequest
    erasure_request.status = "approved"
    erasure_request.completed_at = timezone.now()
    erasure_request.client_file = None  # Already deleted, make explicit
    erasure_request.save(update_fields=["status", "completed_at", "client_file"])

    # 4. Audit log (try/except — audit DB failure shouldn't break erasure)
    try:
        _log_audit(
            user=None,  # System action — all approvers are recorded in ErasureApproval
            action="delete",
            resource_type="client_erasure",
            resource_id=client_pk,
            ip_address=ip_address,
            metadata={
                "erasure_request_id": erasure_request.pk,
                "record_id": record_id,
                "requested_by": erasure_request.requested_by_display,
                "reason_category": erasure_request.reason_category,
                "reason": erasure_request.request_reason,
                "data_summary": erasure_request.data_summary,
                "programs_required": erasure_request.programs_required,
                "approvals": [
                    {"program_id": a.program_id, "approved_by": a.approved_by_display}
                    for a in erasure_request.approvals.all()
                ],
            },
        )
    except Exception:
        logger.error(
            "Failed to write audit log for erasure request %s (client %s)",
            erasure_request.pk, client_pk, exc_info=True,
        )


def _is_admin_fallback(erasure_request, user):
    """Check if this is a valid admin fallback approval (deadlock scenario)."""
    return getattr(user, "is_admin", False) and is_deadlocked(erasure_request)


def _log_audit(user, action, resource_type, resource_id, ip_address, metadata=None):
    """Write an audit log entry to the separate audit database."""
    from apps.audit.models import AuditLog

    AuditLog.objects.using("audit").create(
        event_timestamp=timezone.now(),
        user_id=user.pk if user else None,
        user_display=user.get_display_name() if user else "[system]",
        ip_address=ip_address or "",
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        metadata=metadata or {},
    )
