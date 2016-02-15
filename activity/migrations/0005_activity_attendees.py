# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0001_initial'),
        ('core', '0003_auto_20160115_1337'),
        ('activity', '0004_auto_20160201_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='attendees',
            field=models.ManyToManyField(to='core.Profile', verbose_name='Attendees', through='attendee.Attendee'),
        ),
    ]
