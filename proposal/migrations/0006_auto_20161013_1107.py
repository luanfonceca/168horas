# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0005_auto_20161010_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='brief',
            field=models.TextField(help_text='Max of 300 words.', max_length=5000, verbose_name='Brief', blank=True),
        ),
    ]
