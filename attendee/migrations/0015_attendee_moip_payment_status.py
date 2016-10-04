# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0014_attendee_moip_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='moip_payment_status',
            field=models.CharField(max_length=20, null=True, verbose_name='Moip status', blank=True),
        ),
    ]
