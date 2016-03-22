# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0004_attendee_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='born_at',
            field=models.DateTimeField(null=True, verbose_name='Born At'),
        ),
        migrations.AddField(
            model_name='attendee',
            name='course',
            field=models.CharField(max_length=50, null=True, verbose_name='Course'),
        ),
        migrations.AddField(
            model_name='attendee',
            name='expectations',
            field=models.TextField(null=True, verbose_name='Your expectations'),
        ),
        migrations.AddField(
            model_name='attendee',
            name='startup',
            field=models.CharField(help_text='If you already have one', max_length=50, null=True, verbose_name='Startup'),
        ),
        migrations.AddField(
            model_name='attendee',
            name='university',
            field=models.CharField(max_length=50, null=True, verbose_name='Course'),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='payment_status',
            field=models.SmallIntegerField(default=0, null=True, verbose_name='Payment Status', blank=True, choices=[(0, 'Pending'), (1, 'Canceled'), (2, 'Paid')]),
        ),
    ]
