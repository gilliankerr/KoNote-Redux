"""Admin views for managing registration links and submissions."""
import hashlib

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.clients.models import ClientDetailValue, ClientFile, ClientProgramEnrolment, CustomFieldDefinition

from .forms import RegistrationLinkForm
from .models import RegistrationLink, RegistrationSubmission


def admin_required(view_func):
    """Decorator: 403 if user is not an admin."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin:
            return HttpResponseForbidden("Access denied. Admin privileges required.")
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# --- Registration Link Management ---

@login_required
@admin_required
def link_list(request):
    """List all registration links."""
    links = RegistrationLink.objects.select_related("program", "created_by").all()

    # Add submission counts
    for link in links:
        link.submission_count = link.submissions.count()
        link.pending_count = link.submissions.filter(status="pending").count()

    return render(request, "registration/admin/link_list.html", {
        "links": links,
        "nav_active": "admin",
    })


@login_required
@admin_required
def link_create(request):
    """Create a new registration link."""
    if request.method == "POST":
        form = RegistrationLinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.created_by = request.user
            link.save()
            form.save_m2m()  # Save many-to-many relationships (field_groups)
            messages.success(request, f"Registration link '{link.title}' created.")
            return redirect("registration:registration_link_list")
    else:
        form = RegistrationLinkForm()

    return render(request, "registration/admin/link_form.html", {
        "form": form,
        "editing": False,
        "nav_active": "admin",
    })


@login_required
@admin_required
def link_edit(request, pk):
    """Edit an existing registration link."""
    link = get_object_or_404(RegistrationLink, pk=pk)

    if request.method == "POST":
        form = RegistrationLinkForm(request.POST, instance=link)
        if form.is_valid():
            form.save()
            messages.success(request, f"Registration link '{link.title}' updated.")
            return redirect("registration:registration_link_list")
    else:
        form = RegistrationLinkForm(instance=link)

    return render(request, "registration/admin/link_form.html", {
        "form": form,
        "link": link,
        "editing": True,
        "nav_active": "admin",
    })


@login_required
@admin_required
def link_delete(request, pk):
    """Delete a registration link."""
    link = get_object_or_404(RegistrationLink, pk=pk)

    if request.method == "POST":
        title = link.title
        link.delete()
        messages.success(request, f"Registration link '{title}' deleted.")
        return redirect("registration:registration_link_list")

    return render(request, "registration/admin/link_confirm_delete.html", {
        "link": link,
        "nav_active": "admin",
    })


# --- Submission Management ---

@login_required
def submission_list(request):
    """List all registration submissions with filtering."""
    status_filter = request.GET.get("status", "")

    submissions = RegistrationSubmission.objects.select_related(
        "registration_link",
        "registration_link__program",
        "reviewed_by",
        "client_file",
    ).all()

    if status_filter:
        submissions = submissions.filter(status=status_filter)

    # Check for potential duplicates
    for sub in submissions:
        sub.is_duplicate = _check_duplicate(sub)

    # Count by status for tabs
    status_counts = {
        "all": RegistrationSubmission.objects.count(),
        "pending": RegistrationSubmission.objects.filter(status="pending").count(),
        "approved": RegistrationSubmission.objects.filter(status="approved").count(),
        "rejected": RegistrationSubmission.objects.filter(status="rejected").count(),
        "waitlist": RegistrationSubmission.objects.filter(status="waitlist").count(),
    }

    return render(request, "registration/admin/submission_list.html", {
        "submissions": submissions,
        "status_filter": status_filter,
        "status_counts": status_counts,
        "nav_active": "admin",
    })


@login_required
def submission_detail(request, pk):
    """View details of a registration submission."""
    submission = get_object_or_404(
        RegistrationSubmission.objects.select_related(
            "registration_link",
            "registration_link__program",
            "reviewed_by",
            "client_file",
        ),
        pk=pk,
    )

    # Check for duplicates
    duplicate_client = _find_duplicate_client(submission)

    # Build list of custom field values with labels
    custom_fields = []
    for field_id, value in submission.field_values.items():
        try:
            field_def = CustomFieldDefinition.objects.get(pk=field_id)
            custom_fields.append({
                "name": field_def.name,
                "value": value,
            })
        except CustomFieldDefinition.DoesNotExist:
            custom_fields.append({
                "name": f"Field {field_id}",
                "value": value,
            })

    return render(request, "registration/admin/submission_detail.html", {
        "submission": submission,
        "duplicate_client": duplicate_client,
        "custom_fields": custom_fields,
        "nav_active": "admin",
    })


@login_required
def submission_approve(request, pk):
    """Approve a registration submission and create client record."""
    submission = get_object_or_404(RegistrationSubmission, pk=pk)

    if request.method == "POST":
        if submission.status != "pending":
            messages.error(request, "This submission has already been reviewed.")
            return redirect("registration:submission_detail", pk=pk)

        # 1. Create new ClientFile
        client = ClientFile()
        client.first_name = submission.first_name
        client.last_name = submission.last_name
        client.consent_given_at = submission.submitted_at
        client.consent_type = "registration_form"
        client.save()

        # 2. Copy custom field values
        for field_id, value in submission.field_values.items():
            try:
                field_def = CustomFieldDefinition.objects.get(pk=field_id)
                detail_value = ClientDetailValue(
                    client_file=client,
                    field_def=field_def,
                )
                detail_value.set_value(str(value))
                detail_value.save()
            except CustomFieldDefinition.DoesNotExist:
                pass  # Skip unknown fields

        # 3. Create program enrolment
        ClientProgramEnrolment.objects.create(
            client_file=client,
            program=submission.registration_link.program,
            status="enrolled",
        )

        # 4. Update submission
        submission.status = "approved"
        submission.client_file = client
        submission.reviewed_by = request.user
        submission.reviewed_at = timezone.now()
        submission.save()

        messages.success(
            request,
            f"Approved! Client record created for {client.first_name} {client.last_name}.",
        )
        return redirect("registration:submission_list")

    return redirect("registration:submission_detail", pk=pk)


@login_required
def submission_reject(request, pk):
    """Reject a registration submission."""
    submission = get_object_or_404(RegistrationSubmission, pk=pk)

    if request.method == "POST":
        if submission.status != "pending":
            messages.error(request, "This submission has already been reviewed.")
            return redirect("registration:submission_detail", pk=pk)

        reason = request.POST.get("reason", "").strip()
        if not reason:
            messages.error(request, "A rejection reason is required.")
            return redirect("registration:submission_detail", pk=pk)

        submission.status = "rejected"
        submission.review_notes = reason
        submission.reviewed_by = request.user
        submission.reviewed_at = timezone.now()
        submission.save()

        messages.success(request, "Submission rejected.")
        return redirect("registration:submission_list")

    return redirect("registration:submission_detail", pk=pk)


@login_required
def submission_waitlist(request, pk):
    """Move a submission to waitlist."""
    submission = get_object_or_404(RegistrationSubmission, pk=pk)

    if request.method == "POST":
        if submission.status not in ("pending", "waitlist"):
            messages.error(request, "This submission cannot be waitlisted.")
            return redirect("registration:submission_detail", pk=pk)

        submission.status = "waitlist"
        submission.reviewed_by = request.user
        submission.reviewed_at = timezone.now()
        submission.save()

        messages.success(request, "Submission moved to waitlist.")
        return redirect("registration:submission_list")

    return redirect("registration:submission_detail", pk=pk)


# --- Helper Functions ---

def _check_duplicate(submission):
    """Check if a submission might be a duplicate (by email hash)."""
    if not submission.email_hash:
        return False

    # Check existing clients with same email hash
    # First, check other submissions
    other_submissions = RegistrationSubmission.objects.filter(
        email_hash=submission.email_hash,
        status="approved",
    ).exclude(pk=submission.pk).exists()

    return other_submissions


def _find_duplicate_client(submission):
    """Find an existing client that matches this submission."""
    if not submission.email_hash:
        return None

    # Look for approved submissions with same email hash that have a client
    duplicate_submission = RegistrationSubmission.objects.filter(
        email_hash=submission.email_hash,
        status="approved",
        client_file__isnull=False,
    ).exclude(pk=submission.pk).first()

    if duplicate_submission:
        return duplicate_submission.client_file

    return None
