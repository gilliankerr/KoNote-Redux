# Phase 4: Progress note views
"""Views for progress notes — quick notes, full notes, timeline, cancellation."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from apps.clients.models import ClientFile, ClientProgramEnrolment
from apps.programs.models import UserProgramRole

from .forms import QuickNoteForm
from .models import ProgressNote


def _get_client_or_403(request, client_id):
    """Return client if user has access, otherwise 403."""
    client = get_object_or_404(ClientFile, pk=client_id)
    user = request.user
    if user.is_admin:
        return client
    user_program_ids = set(
        UserProgramRole.objects.filter(user=user, status="active")
        .values_list("program_id", flat=True)
    )
    client_program_ids = set(
        ClientProgramEnrolment.objects.filter(client_file=client, status="enrolled")
        .values_list("program_id", flat=True)
    )
    if user_program_ids & client_program_ids:
        return client
    return None


def _get_author_program(user, client):
    """Return the first program the user shares with this client, or None."""
    user_program_ids = set(
        UserProgramRole.objects.filter(user=user, status="active")
        .values_list("program_id", flat=True)
    )
    client_program_ids = set(
        ClientProgramEnrolment.objects.filter(client_file=client, status="enrolled")
        .values_list("program_id", flat=True)
    )
    shared = user_program_ids & client_program_ids
    if shared:
        from apps.programs.models import Program
        return Program.objects.filter(pk__in=shared).first()
    return None


@login_required
def note_list(request, client_id):
    """Notes timeline for a client — full implementation in Step 4."""
    client = _get_client_or_403(request, client_id)
    if client is None:
        return HttpResponseForbidden("You do not have access to this client.")

    notes = ProgressNote.objects.filter(client_file=client).select_related("author", "author_program")
    return render(request, "notes/note_list.html", {
        "client": client,
        "notes": notes,
    })


@login_required
def quick_note_create(request, client_id):
    """Create a quick note for a client."""
    client = _get_client_or_403(request, client_id)
    if client is None:
        return HttpResponseForbidden("You do not have access to this client.")

    if request.method == "POST":
        form = QuickNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.client_file = client
            note.note_type = "quick"
            note.author = request.user
            note.author_program = _get_author_program(request.user, client)
            note.save()
            messages.success(request, "Quick note saved.")
            return redirect("notes:note_list", client_id=client.pk)
    else:
        form = QuickNoteForm()

    return render(request, "notes/quick_note_form.html", {
        "form": form,
        "client": client,
    })
