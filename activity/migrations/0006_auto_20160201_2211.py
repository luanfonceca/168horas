# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0005_activity_attendees'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='capacity',
            field=models.IntegerField(default=50, null=True, verbose_name='Capacity', blank=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='price',
            field=models.DecimalField(null=True, verbose_name='Price', max_digits=10, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='attendees',
            field=models.ManyToManyField(related_name='activities+', verbose_name='Attendees', through='attendee.Attendee', to='core.Profile'),
        ),
    ]
