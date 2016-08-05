# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0010_activity_place_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='embedded_schedule',
            field=models.TextField(max_length=2000, null=True, verbose_name='Embedded Schedule', blank=True),
        ),
    ]
