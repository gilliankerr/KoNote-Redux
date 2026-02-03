# Generated manually for UX13: Add all_day toggle to event form

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='all_day',
            field=models.BooleanField(default=False, help_text='If true, only the date is stored; time is ignored.'),
        ),
    ]
