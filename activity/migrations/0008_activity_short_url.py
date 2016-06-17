# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0007_activity_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='short_url',
            field=models.SlugField(blank=True, help_text='Result will be like: http://168h.com.br/my-activity/', null=True, verbose_name='Short url'),
        ),
    ]
