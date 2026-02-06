"""Data migration: backfill validation_type for existing custom fields (I18N-FIX2).

Sets validation_type based on known field names so existing deployments
get correct validation without requiring a manual update.
"""
from django.db import migrations


def set_validation_types(apps, schema_editor):
    CustomFieldDefinition = apps.get_model("clients", "CustomFieldDefinition")

    # Known postal code field names (English and French)
    POSTAL = ["Postal Code", "Code postal"]
    # Known phone field names
    PHONE = [
        "Primary Phone",
        "Secondary Phone",
        "Emergency Contact Phone",
        "Parent/Guardian Phone",
        "Secondary Parent/Guardian Phone",
    ]

    updated_postal = CustomFieldDefinition.objects.filter(
        name__in=POSTAL
    ).update(validation_type="postal_code")

    updated_phone = CustomFieldDefinition.objects.filter(
        name__in=PHONE
    ).update(validation_type="phone")

    print(f"  Set {updated_postal} postal code field(s), {updated_phone} phone field(s)")


def reverse(apps, schema_editor):
    CustomFieldDefinition = apps.get_model("clients", "CustomFieldDefinition")
    CustomFieldDefinition.objects.filter(
        validation_type__in=["postal_code", "phone"]
    ).update(validation_type="none")


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0008_customfielddefinition_validation_type"),
    ]

    operations = [
        migrations.RunPython(set_validation_types, reverse),
    ]
