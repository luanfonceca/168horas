# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_auto_20151120_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='photo',
            field=models.ImageField(help_text=b'Images in the resolution: 300x300.', null=True, upload_to=b'photos/', blank=True),
        ),
    ]
