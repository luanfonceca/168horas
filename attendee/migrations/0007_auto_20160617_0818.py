# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0006_attendee_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='moip_code',
            field=models.CharField(max_length=20, null=True, verbose_name='Moip code', blank=True),
        ),
        migrations.AddField(
            model_name='attendee',
            name='moip_payment_type',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Status', choices=[(b'DebitoBancario', 'Debito bancario'), (b'FinanciamentoBancario', 'Financiamento bancario'), (b'BoletoBancario', 'Boleto bancario'), (b'CartaoDeCredito', 'Cartao de credito'), (b'CartaoDeDebito', 'Cartao de debito'), (b'CarteiraMoIP', 'Cartira moip'), (b'NaoDefinida', 'Nao definida')]),
        ),
        migrations.AddField(
            model_name='attendee',
            name='moip_status',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Status', choices=[(1, 'Autorizado'), (2, 'Iniciado'), (3, 'Boleto impresso'), (4, 'Concluido'), (5, 'Em analise'), (6, 'Estornado')]),
        ),
    ]
