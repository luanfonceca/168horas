# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0014_activity_activities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='status',
            field=models.SmallIntegerField(default=3, verbose_name='Status', choices=[(6, 'Open Proposals'), (0, 'Draft'), (1, 'Private'), (2, 'Pre-sale'), (3, 'Published'), (4, 'Soldout'), (5, 'Closed')]),
        ),
    ]
