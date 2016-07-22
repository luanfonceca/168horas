# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0010_auto_20160722_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='course',
            field=models.CharField(max_length=200, null=True, verbose_name='Em caso de Ensino Superior ou T\xe9cnico, qual curso?', blank=True),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='name',
            field=models.CharField(max_length=300, verbose_name='Full Name'),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='scholarship_term',
            field=models.CharField(help_text='Ex.: 3\xba ano; 6\xba per\xedodo', max_length=50, null=True, verbose_name='Ano/Per\xedodo', blank=True),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='where_know_us',
            field=models.SmallIntegerField(null=True, verbose_name='Como ficou sabendo do SNE 2015?', choices=[(0, 'WhatsApp'), (1, 'Facebook'), (2, 'Twitter'), (2, 'Instagram'), (2, 'Email'), (3, 'Boca a Boca')]),
        ),
    ]
