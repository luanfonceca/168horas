# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_auto_20160126_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='photo',
            field=models.ImageField(help_text='Images in the resolution: 400x400.', upload_to=b'photos/', null=True, verbose_name='Event photo', blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='scheduled_date',
            field=models.DateField(null=True, verbose_name='Date', blank=True),
        ),
    ]
