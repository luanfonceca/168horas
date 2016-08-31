# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0013_auto_20160827_0553'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='moip_payment_id',
            field=models.CharField(max_length=20, null=True, verbose_name='Moip payment', blank=True),
        ),
    ]
