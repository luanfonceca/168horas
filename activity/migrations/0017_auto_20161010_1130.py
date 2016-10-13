# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0016_auto_20161004_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='organizers',
            field=models.ManyToManyField(related_name='managed_activities', verbose_name='Organizers', to='core.Profile'),
        ),
    ]
