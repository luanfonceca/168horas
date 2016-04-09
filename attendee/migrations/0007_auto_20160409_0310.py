# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0006_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendee',
            name='born_at',
        ),
        migrations.RemoveField(
            model_name='attendee',
            name='course',
        ),
        migrations.RemoveField(
            model_name='attendee',
            name='expectations',
        ),
        migrations.RemoveField(
            model_name='attendee',
            name='startup',
        ),
        migrations.RemoveField(
            model_name='attendee',
            name='university',
        ),
    ]
