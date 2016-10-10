# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0004_auto_20160928_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='pre_requisitos',
            field=models.TextField(max_length=2000, null=True, verbose_name='Pr\xe9-requisitos'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='carga_horaria',
            field=models.IntegerField(default=0, null=True, verbose_name='Carga hor\xe1ria', blank=True, choices=[(0, 'Duas Horas'), (1, 'Quatro Horas'), (2, 'Seis Horas')]),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='publico',
            field=models.CharField(max_length=300, null=True, verbose_name='Tipo de P\xfablico'),
        ),
    ]
