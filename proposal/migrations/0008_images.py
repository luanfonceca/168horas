# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0007_auto_20161103_2138'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'', null=True, verbose_name='File', blank=True)),
                ('proposal', models.ForeignKey(related_name='images', to='proposal.Proposal')),
            ],
            options={
                'verbose_name': 'Images',
                'verbose_name_plural': 'Imagess',
            },
        ),
    ]
