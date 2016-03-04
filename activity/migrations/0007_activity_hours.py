# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0006_auto_20160201_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='hours',
            field=models.IntegerField(help_text='Total of hours to be used in the Certificate.', null=True, blank=True),
        ),
    ]
