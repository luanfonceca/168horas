# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0013_auto_20161004_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='email',
            field=models.EmailField(max_length=300, verbose_name='Email'),
        ),
    ]
