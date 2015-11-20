# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_event_add_link_and_scheduled_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='photo',
            field=models.ImageField(null=True, upload_to=b'photos/', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='categories',
            field=models.ManyToManyField(related_name='events', verbose_name='Categorias', to='category.Category'),
        ),
        migrations.AlterField(
            model_name='event',
            name='scheduled_date',
            field=models.DateField(null=True, verbose_name='Data', blank=True),
        ),
    ]
