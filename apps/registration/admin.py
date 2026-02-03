"""Django admin registration for registration models."""
from django.contrib import admin

from .models import RegistrationLink, RegistrationSubmission


@admin.register(RegistrationLink)
class RegistrationLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "program", "slug", "is_active", "created_at")
    list_filter = ("is_active", "program", "auto_approve")
    search_fields = ("title", "slug")
    readonly_fields = ("slug", "created_at", "created_by")
    filter_horizontal = ("field_groups",)


@admin.register(RegistrationSubmission)
class RegistrationSubmissionAdmin(admin.ModelAdmin):
    # Encrypted PII fields excluded — use property accessors in readonly
    list_display = ("reference_number", "registration_link", "status", "submitted_at")
    list_filter = ("status", "registration_link")
    search_fields = ("reference_number", "email_hash")
    readonly_fields = ("reference_number", "email_hash", "submitted_at", "reviewed_at")
