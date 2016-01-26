# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20160115_1337'),
        ('category', '0002_auto_20151229_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'title', verbose_name='slug', editable=False, blank=True)),
                ('link', models.URLField(max_length=300, null=True, verbose_name='Link', blank=True)),
                ('scheduled_date', models.DateField(null=True, verbose_name='Data', blank=True)),
                ('created_at', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('is_published', models.BooleanField(default=True, verbose_name='Is Published')),
                ('is_public', models.BooleanField(default=True, verbose_name='Is Public')),
                ('is_organizer', models.BooleanField(default=False, verbose_name='Is Organizer')),
                ('is_online', models.BooleanField(default=False)),
                ('photo', models.ImageField(help_text=b'Images in the resolution: 400x400.', null=True, upload_to=b'photos/', blank=True)),
                ('location', models.CharField(max_length=500, null=True, verbose_name='Location', blank=True)),
                ('categories', models.ManyToManyField(related_name='activities', verbose_name='Categorias', to='category.Category')),
                ('created_by', models.ForeignKey(related_name='activities', verbose_name='Created by', blank=True, to='core.Profile', null=True)),
            ],
            options={
                'verbose_name': 'Activity',
                'verbose_name_plural': 'Activities',
            },
        ),
    ]
