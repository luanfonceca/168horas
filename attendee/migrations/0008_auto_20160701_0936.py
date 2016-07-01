# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0007_auto_20160617_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='moip_status',
            field=models.SmallIntegerField(default=0, null=True, verbose_name='Status', blank=True, choices=[(0, 'Pendente de pagamento'), (1, 'Autorizado'), (2, 'Iniciado'), (3, 'Boleto impresso'), (4, 'Concluido'), (5, 'Cancelado'), (6, 'Em analise'), (7, 'Estornado'), (8, 'Confirmado pelo Organizador')]),
        ),
    ]
