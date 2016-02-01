# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20160115_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='categories',
            field=models.ManyToManyField(to='category.Category', verbose_name='Categories'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='digital_signature',
            field=models.ImageField(help_text=b'PNG signatures in the resolution: 200x200.', upload_to=b'signatures/', null=True, verbose_name='Digital Signature', blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='organizer_email',
            field=models.EmailField(max_length=200, null=True, verbose_name='Organizer Email', blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='organizer_name',
            field=models.CharField(max_length=200, null=True, verbose_name='Organizer Name', blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='organizer_phone',
            field=models.CharField(max_length=30, null=True, verbose_name='Organizer Phone', blank=True),
        ),
    ]
