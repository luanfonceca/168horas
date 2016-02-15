# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

import attendee.models

class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='attended_at',
            field=models.DateTimeField(null=True, verbose_name='Attended At', blank=True),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='code',
            field=models.CharField(default=attendee.models.code_generate, max_length=10, verbose_name='Code'),
        ),
        migrations.AlterUniqueTogether(
            name='attendee',
            unique_together=set([('activity', 'profile')]),
        ),
    ]
