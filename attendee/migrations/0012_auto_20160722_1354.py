# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0011_auto_20160722_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='age_rage',
            field=models.SmallIntegerField(default=0, null=True, verbose_name='Sua idade \xe9', choices=[(0, 'Menor que 15 anos'), (1, 'Entre 15 e 23 anos'), (2, 'Maior que 23 anos')]),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='already_joinned_our_program',
            field=models.SmallIntegerField(default=0, null=True, verbose_name='J\xe1 participou ou participa do programa Miniempresa?', choices=[(0, 'Sim'), (1, 'N\xe3o')]),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='already_know_us',
            field=models.SmallIntegerField(default=0, null=True, verbose_name='J\xe1 conhecia o Nexa ou a Junior Achievement?', choices=[(0, 'Sim'), (1, 'N\xe3o'), (2, 'J\xe1 ouvi falar')]),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='join_previous_editions',
            field=models.SmallIntegerField(default=0, null=True, verbose_name='Voc\xea participou de alguma das edi\xe7\xf5es anteriores do SNE?', choices=[(0, 'Sim'), (1, 'N\xe3o')]),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='partner_profile',
            field=models.SmallIntegerField(default=0, help_text='S\xf3cio, caso tenha realizado o cadastro; Achiever, caso esteja participando do programa Miniempresa; Ex-achiever, caso tenha feito o programa Miniempresa; Volunt\xe1rio JARN; Externo, caso n\xe3o se aplique aos anteriores.', null=True, verbose_name='Voc\xea \xe9...', choices=[(0, 'S\xf3cio do Nexa RN'), (1, 'Achiever'), (2, 'Ex-achiever'), (3, 'Externo'), (4, 'Volunt\xe1rio JARN')]),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='where_know_us',
            field=models.SmallIntegerField(default=0, null=True, verbose_name='Como ficou sabendo do SNE 2015?', choices=[(0, 'WhatsApp'), (1, 'Facebook'), (2, 'Twitter'), (2, 'Instagram'), (2, 'Email'), (3, 'Boca a Boca')]),
        ),
    ]
