# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0009_auto_20160722_1130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendee',
            name='which_one',
        ),
        migrations.AddField(
            model_name='attendee',
            name='which_company',
            field=models.CharField(help_text='(Ex.: BiggLimp S.A./E.; Lumiere S.A/E.; Life tech S.A./E)', max_length=200, null=True, verbose_name='Qual Miniempresa? Em qual ano?', blank=True),
        ),
        migrations.AddField(
            model_name='attendee',
            name='which_edition',
            field=models.CharField(help_text='(Edi\xe7\xe3o I, 2012; Edi\xe7\xe3o II, 2013; Edi\xe7\xe3o III, 2014; Edi\xe7\xe3o IV 2015)', max_length=200, null=True, verbose_name='Quais?', blank=True),
        ),
    ]
