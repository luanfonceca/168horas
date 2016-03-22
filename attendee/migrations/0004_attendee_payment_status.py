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
            name='payment_status',
            field=models.SmallIntegerField(default=2, null=True, verbose_name='Payment Status', blank=True, choices=[(0, b'pending'), (1, b'canceled'), (2, b'paid')]),
        ),
    ]
