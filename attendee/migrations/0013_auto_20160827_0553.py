# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0012_auto_20160722_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='moip_customer_id',
            field=models.CharField(max_length=20, null=True, verbose_name='Moip customer', blank=True),
        ),
        migrations.AddField(
            model_name='attendee',
            name='moip_order_id',
            field=models.CharField(max_length=20, null=True, verbose_name='Moip order', blank=True),
        ),
    ]
