# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0006_auto_20161013_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='phone',
            field=models.CharField(max_length=30, null=True, verbose_name='Phone', blank=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='camera',
            field=models.CharField(max_length=200, null=True, verbose_name='C\xe2mera utilizada na capta\xe7\xe3o da imagem'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='ferramenta',
            field=models.CharField(max_length=200, null=True, verbose_name='Programa utilizado no tratamento da imagem'),
        ),
    ]
