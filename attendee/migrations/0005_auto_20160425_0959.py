# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0004_attendee_educational_institution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='name',
            field=models.CharField(max_length=300, verbose_name='Name'),
        ),
    ]
