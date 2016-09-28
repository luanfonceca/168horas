# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0013_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='activities',
            field=models.ManyToManyField(related_name='compilations+', verbose_name='Compilations', to='activity.Activity', blank=True),
        ),
    ]
