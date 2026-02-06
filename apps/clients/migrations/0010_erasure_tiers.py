"""Add tiered erasure support: erasure_tier, erasure_code on ErasureRequest;
is_anonymised on ClientFile. Backfill existing approved erasures as full_erasure.
"""
from django.db import migrations, models


def backfill_existing_erasures(apps, schema_editor):
    """Set erasure_tier='full_erasure' on any existing completed erasure requests,
    and generate erasure_codes for all existing requests."""
    ErasureRequest = apps.get_model("clients", "ErasureRequest")
    for i, er in enumerate(ErasureRequest.objects.all().order_by("requested_at"), start=1):
        updates = {}
        if er.status == "approved":
            updates["erasure_tier"] = "full_erasure"
        if not er.erasure_code:
            year = er.requested_at.year if er.requested_at else 2026
            updates["erasure_code"] = f"ER-{year}-{i:03d}"
        if updates:
            ErasureRequest.objects.filter(pk=er.pk).update(**updates)


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0009_backfill_validation_types"),
    ]

    operations = [
        # Add is_anonymised to ClientFile
        migrations.AddField(
            model_name="clientfile",
            name="is_anonymised",
            field=models.BooleanField(
                default=False,
                help_text="True after PII has been stripped. Record kept for statistical purposes.",
            ),
        ),
        # Add erasure_tier to ErasureRequest
        migrations.AddField(
            model_name="erasurerequest",
            name="erasure_tier",
            field=models.CharField(
                choices=[
                    ("anonymise", "Anonymise"),
                    ("anonymise_purge", "Anonymise + Purge Notes"),
                    ("full_erasure", "Full Erasure"),
                ],
                default="anonymise",
                help_text="Level of data erasure: anonymise (default), purge notes, or full delete.",
                max_length=20,
            ),
        ),
        # Add erasure_code to ErasureRequest (temporarily allow blank for backfill)
        migrations.AddField(
            model_name="erasurerequest",
            name="erasure_code",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Auto-generated reference code, e.g. ER-2026-001.",
                max_length=20,
                unique=True,
            ),
        ),
        # Update status choices to include "anonymised"
        migrations.AlterField(
            model_name="erasurerequest",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending Approval"),
                    ("anonymised", "Approved — Data Anonymised"),
                    ("approved", "Approved — Data Erased"),
                    ("rejected", "Rejected"),
                    ("cancelled", "Cancelled"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
        # Backfill existing records
        migrations.RunPython(backfill_existing_erasures, migrations.RunPython.noop),
    ]
