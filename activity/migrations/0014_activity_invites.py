# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0003_auto_20151126_1523'),
        ('activity', '0013_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='invites',
            field=models.ManyToManyField(related_name='activities', verbose_name='Invites', to='invitations.Invitation'),
        ),
    ]
