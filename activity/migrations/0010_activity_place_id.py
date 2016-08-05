# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0009_activity_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='place_id',
            field=models.CharField(max_length=50, null=True, verbose_name='Place id', blank=True),
        ),
    ]
