# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='document',
            field=models.FileField(upload_to=b'', null=True, verbose_name='Document', blank=True),
        ),
    ]
