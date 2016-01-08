# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0007_event_is_online'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='photo',
            field=models.ImageField(help_text=b'Images in the resolution: 400x400.', null=True, upload_to=b'photos/', blank=True),
        ),
    ]
