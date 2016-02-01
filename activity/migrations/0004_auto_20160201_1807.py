# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0003_auto_20160126_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='categories',
            field=models.ManyToManyField(related_name='activities', verbose_name='Categories', to='category.Category'),
        ),
    ]
