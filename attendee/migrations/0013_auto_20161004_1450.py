# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0012_auto_20160722_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='course',
            field=models.CharField(max_length=200, null=True, verbose_name='Em caso de Ensino Superior ou T\xe9cnico, qual curso?'),
        ),
    ]
