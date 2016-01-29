# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20160115_1337'),
        ('activity', '0003_auto_20160126_0757'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cpf', models.CharField(max_length=14, null=True, verbose_name=b'CPF', blank=True)),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Name', blank=True)),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='Email', blank=True)),
                ('phone', models.CharField(max_length=50, verbose_name='Phone', blank=True)),
                ('code', models.CharField(default=b'0295BEDO0G', max_length=10, verbose_name='Code')),
                ('created_at', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('attended_at', models.DateTimeField(null=True, blank=True)),
                ('activity', models.ForeignKey(to='activity.Activity')),
                ('profile', models.ForeignKey(to='core.Profile')),
            ],
            options={
                'verbose_name': 'Attendee',
                'verbose_name_plural': 'Attendees',
            },
        ),
    ]
