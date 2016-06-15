# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def confirm_all_attendees(apps, schema_editor):
    Attendee = apps.get_model('attendee', 'Attendee')
    db_alias = schema_editor.connection.alias
    Attendee.objects.using(db_alias).update(
        status=1  # Confirmed Status
    )


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0005_auto_20160425_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='status',
            field=models.SmallIntegerField(default=0, verbose_name='Status', choices=[(0, 'Pending'), (1, 'Confirmed'), (2, 'Canceled')]),
        ),
        migrations.RunPython(confirm_all_attendees)
    ]
