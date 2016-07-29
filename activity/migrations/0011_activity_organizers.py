# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_authors_to_organizers(apps, schema_editor):
    Activity = apps.get_model('activity', 'Activity')

    for activity in Activity.objects.exclude(created_by__isnull=True):
        activity.organizers.add(activity.created_by)


def reverse_add_authors_to_organizers(apps, schema_editor):
    Activity = apps.get_model('activity', 'Activity')

    for activity in Activity.objects.exclude():
        activity.organizers.clear()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20160201_1807'),
        ('activity', '0010_activity_place_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='organizers',
            field=models.ManyToManyField(related_name='managed_activities', verbose_name='Categories', to='core.Profile'),
        ),
        migrations.RunPython(
            add_authors_to_organizers,
            reverse_code=reverse_add_authors_to_organizers
        )
    ]
