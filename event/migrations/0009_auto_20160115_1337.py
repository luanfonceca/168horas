# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20160115_1337'),
        ('event', '0008_auto_20160108_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='created_by',
            field=models.ForeignKey(related_name='events', verbose_name='Created by', blank=True, to='core.Profile', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='is_organizer',
            field=models.BooleanField(default=False, verbose_name='Is Organizer'),
        ),
    ]
