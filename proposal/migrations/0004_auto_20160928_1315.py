# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0003_auto_20160928_1309'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300, verbose_name='Name')),
                ('email', models.EmailField(max_length=300, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Author',
            },
        ),
        migrations.AlterField(
            model_name='proposal',
            name='ementa',
            field=models.TextField(max_length=1000, verbose_name='Ementa'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='institution',
            field=models.CharField(max_length=200, null=True, verbose_name='Institution'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='justificativa',
            field=models.TextField(max_length=1000, verbose_name='Justificativa'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='materiais',
            field=models.TextField(max_length=1000, verbose_name='Materiais necess\xe1rios'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='objetivos',
            field=models.TextField(max_length=1000, verbose_name='Objetivos'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='publico',
            field=models.CharField(max_length=300, null=True, verbose_name='Tipo de Publico'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='quantidade_de_vagas',
            field=models.IntegerField(null=True, verbose_name='Quantidade de Vagas'),
        ),
        migrations.AddField(
            model_name='author',
            name='proposal',
            field=models.ForeignKey(related_name='authors', to='proposal.Proposal'),
        ),
    ]
