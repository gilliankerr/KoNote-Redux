# Generated manually for I18N2 - French terminology support

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_settings", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="terminologyoverride",
            name="display_value_fr",
            field=models.CharField(
                blank=True,
                default="",
                help_text="French translation. Leave blank to use English value.",
                max_length=255,
            ),
        ),
    ]
