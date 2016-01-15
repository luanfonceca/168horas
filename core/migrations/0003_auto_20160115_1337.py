# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20151217_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cnpj',
            field=models.CharField(max_length=18, null=True, verbose_name=b'CNPJ', blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='cpf',
            field=models.CharField(max_length=14, null=True, verbose_name=b'CPF', blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='digital_signature',
            field=models.ImageField(help_text=b'PNG signatures in the resolution: 200x200.', null=True, upload_to=b'signatures/', blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='organizer_email',
            field=models.EmailField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='organizer_name',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='organizer_phone',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
