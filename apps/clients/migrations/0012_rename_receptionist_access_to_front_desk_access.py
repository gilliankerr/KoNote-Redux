"""Rename receptionist_access to front_desk_access (DB-TERM1).

The role was renamed from "Receptionist" to "Front Desk" — this aligns
the database column name with the current terminology.
"""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0011_add_receipt_downloaded_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customfielddefinition',
            old_name='receptionist_access',
            new_name='front_desk_access',
        ),
    ]
