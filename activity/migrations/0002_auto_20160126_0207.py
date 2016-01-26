# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_activities(apps, schema_editor):
    Activity = apps.get_model('activity', 'Activity')
    Event = apps.get_model('event', 'Event')

    for event in Event.objects.all():
        activity = Activity.objects.create(
            link=event.link,
            scheduled_date=event.scheduled_date,
            created_at=event.created_at,
            is_published=event.is_published,
            is_public=event.is_public,
            is_organizer=event.is_organizer,
            is_online=event.is_online,
            photo=event.photo,
            location=event.location,
            created_by=event.created_by,
        )
        activity.categories.add(*event.categories.all())


def reverse_create_activities(apps, schema_editor):
    Activity = apps.get_model('activity', 'Activity')
    Activity.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('activity', '0001_initial'),
        ('event', '0009_auto_20160115_1337'),
    ]

    operations = [
        migrations.RunPython(
            code=create_activities,
            reverse_code=reverse_create_activities),
    ]
