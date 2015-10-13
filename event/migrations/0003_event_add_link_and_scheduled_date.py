# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_event_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='link',
            field=models.URLField(max_length=300, null=True, verbose_name='Link', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='scheduled_date',
            field=models.DateField(null=True, verbose_name='Date', blank=True),
        ),
    ]
