# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0002_proposal_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='carga_horaria',
            field=models.IntegerField(default=0, null=True, verbose_name='Carga horaria', blank=True, choices=[(0, 'Duas Horas'), (1, 'Quatro Horas'), (2, 'Seis Horas')]),
        ),
        migrations.AddField(
            model_name='proposal',
            name='ementa',
            field=models.TextField(max_length=1000, verbose_name='Ementa', blank=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='institution',
            field=models.CharField(max_length=200, null=True, verbose_name='Institution', blank=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='justificativa',
            field=models.TextField(max_length=1000, verbose_name='Justificativa', blank=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='materiais',
            field=models.TextField(max_length=1000, verbose_name='Materiais necess\xe1rios', blank=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='objetivos',
            field=models.TextField(max_length=1000, verbose_name='Objetivos', blank=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='publico',
            field=models.CharField(max_length=300, null=True, verbose_name='Tipo de Publico', blank=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='quantidade_de_vagas',
            field=models.IntegerField(null=True, verbose_name='Quantidade de Vagas', blank=True),
        ),
    ]
