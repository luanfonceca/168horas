# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_event_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_online',
            field=models.BooleanField(default=False),
        ),
    ]
