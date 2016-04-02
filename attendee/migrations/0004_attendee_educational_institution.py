# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0003_auto_20160215_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='educational_institution',
            field=models.CharField(max_length=200, null=True, verbose_name='Educational Institution', blank=True),
        ),
    ]
