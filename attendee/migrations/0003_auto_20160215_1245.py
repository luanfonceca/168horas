# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0002_auto_20160201_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='cpf',
            field=models.CharField(default=None, max_length=14, verbose_name=b'CPF'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attendee',
            name='email',
            field=models.EmailField(default=None, max_length=254, verbose_name='Email'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attendee',
            name='name',
            field=models.CharField(default=None, max_length=200, verbose_name='Name'),
            preserve_default=False,
        ),
    ]
