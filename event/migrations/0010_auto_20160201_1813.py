# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_auto_20160115_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='scheduled_date',
            field=models.DateField(null=True, verbose_name='Date', blank=True),
        ),
    ]
