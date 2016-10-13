# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def update_end_scheduled_date(apps, schema_editor):
    Activity = apps.get_model('activity', 'Activity')

    for activity in Activity.objects.filter(scheduled_date__isnull=False):
        activity.start_scheduled_date = activity.scheduled_date
        activity.end_scheduled_date = activity.start_scheduled_date


def reverse_update_end_scheduled_date(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0015_auto_20160928_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='end_scheduled_date',
            field=models.DateField(null=True, verbose_name='End Date', blank=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='start_scheduled_date',
            field=models.DateField(null=True, verbose_name='Start Date', blank=True),
        ),
        migrations.RunPython(
            code=update_end_scheduled_date,
            reverse_code=reverse_update_end_scheduled_date,
        ),
        migrations.RemoveField(
            model_name='activity',
            name='scheduled_date',
        )
    ]
