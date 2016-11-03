# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0012_activity_organizers'),
        ('core', '0004_auto_20160201_1807'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300, verbose_name='Title')),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, populate_from='title', max_length=340, blank=True, unique=True, overwrite=True)),
                ('brief', models.TextField(help_text='Max of 300 words.', max_length=1000, verbose_name='Brief', blank=True)),
                ('created_at', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('area', models.CharField(max_length=100, verbose_name='Area', choices=[('codigos-e-linguagens', 'C\xf3digos e Linguagenns'), ('ciencias-da-natureza-e-suas-tecnologias', 'Ci\xeancias da Natureza e Suas Tecnologias'), ('eletronica', 'Eletr\xf4nica'), ('gestao-e-negocios', 'Gest\xe3o e Neg\xf3cios'), ('informatica', 'Inform\xe1tica'), ('marketing', 'Marketing'), ('educacao', 'Educa\xe7\xe3o')])),
                ('activity', models.ForeignKey(related_name='proposals', to='activity.Activity')),
                ('created_by', models.ForeignKey(related_name='proposals', to='core.Profile')),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name': 'Proposal',
                'verbose_name_plural': 'Proposals',
            },
        ),
    ]
