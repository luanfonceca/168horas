# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import datetime
from django.utils.dateformat import format as dateformat

from django_extensions.db.fields import CreationDateTimeField


def code_generate(size=10):
    return ''.join(
        random.choice(
            string.ascii_uppercase + string.digits
        ) for x in range(size))


class Attendee(models.Model):
    PENDING, CONFIRMED, CANCELED = range(3)
    STATUS_CHOICES = (
        (PENDING, _('Pending')),
        (CONFIRMED, _('Confirmed')),
        (CANCELED, _('Canceled')),
    )

    # autorizado      1  Pagamento ja foi realizado porem ainda nao foi
    #                    creditado na Carteira MoIP recebedora
    #                    (devido ao floating da forma de pagamento)
    # iniciado        2  Pagamento esta sendo realizado ou janela do
    #                    navegador foi fechada (pagamento abandonado)
    # boleto impresso 3  Boleto foi impresso e ainda nao foi pago
    # concluido       4  Pagamento ja foi realizado e dinheiro
    #                    ja foi creditado na Carteira MoIP recebedora
    # cancelado       5  Pagamento foi cancelado pelo pagador,
    #                    instituicao de pagamento, MoIP ou recebedor
    #                    antes de ser concluido
    # em analise      6  Pagamento foi realizado com cartao de credito e
    #                    autorizado, porem esta em analise pela Equipe MoIP.
    #                    Nao existe garantia de que sera concluido
    # estornado       7  Pagamento foi estornado pelo pagador, recebedor,
    #                    instituicao de pagamento ou MoIP
    (PENDENTE_DE_PAGAMENTO, AUTORIZADO, INICIADO,
     BOLETO_IMPRESSO, CONCLUIDO, CANCELADO, EM_ANALISE,
     ESTORNADO, CONFIRMADO_PELO_ORGANIZADOR) = range(0, 9)
    MOIP_STATUS_CHOICES = (
        (PENDENTE_DE_PAGAMENTO, _('Pendente de pagamento')),
        (AUTORIZADO, _('Autorizado')),
        (INICIADO, _('Iniciado')),
        (BOLETO_IMPRESSO, _('Boleto impresso')),
        (CONCLUIDO, _('Concluido')),
        (CANCELADO, _('Cancelado')),
        (EM_ANALISE, _('Em analise')),
        (ESTORNADO, _('Estornado')),
        (CONFIRMADO_PELO_ORGANIZADOR, _('Confirmado pelo Organizador')),
    )

    DEBITO_BANCARIO = 'DebitoBancario'
    FINANCIAMENTO_BANCARIO = 'FinanciamentoBancario'
    BOLETO_BANCARIO = 'BoletoBancario'
    CARTAO_DE_CREDITO = 'CartaoDeCredito'
    CARTAO_DE_DEBITO = 'CartaoDeDebito'
    CARTEIRA_MOIP = 'CarteiraMoIP'
    NAO_DEFINIDA = 'NaoDefinida'
    MOIP_PAYMENT_TYPE_CHOICES = (
        (DEBITO_BANCARIO, _('Debito bancario')),
        (FINANCIAMENTO_BANCARIO, _('Financiamento bancario')),
        (BOLETO_BANCARIO, _('Boleto bancario')),
        (CARTAO_DE_CREDITO, _('Cartao de credito')),
        (CARTAO_DE_DEBITO, _('Cartao de debito')),
        (CARTEIRA_MOIP, _('Cartira moip')),
        (NAO_DEFINIDA, _('Nao definida')),
    )

    name = models.CharField(_('Name'), max_length=300)
    cpf = models.CharField('CPF', max_length=14)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Phone'), max_length=50, blank=True)
    educational_institution = models.CharField(
        _('Educational Institution'), max_length=200, null=True, blank=True)
    code = models.CharField(_('Code'), max_length=10, default=code_generate)
    created_at = CreationDateTimeField(_(u'Created At'))
    attended_at = models.DateTimeField(
        _(u'Attended At'), null=True, blank=True)
    last_updated_at = models.DateTimeField(
        _(u'Last Updated At'), null=True, blank=True)
    status = models.SmallIntegerField(
        _('Status'), choices=STATUS_CHOICES, default=PENDING)
    moip_status = models.SmallIntegerField(
        _('Status'), choices=MOIP_STATUS_CHOICES,
        null=True, blank=True, default=PENDENTE_DE_PAGAMENTO)
    moip_payment_type = models.CharField(
        _('Status'), max_length=32, choices=MOIP_PAYMENT_TYPE_CHOICES,
        null=True, blank=True)
    moip_code = models.CharField(
        _('Moip code'), max_length=20, null=True, blank=True)

    # relations
    activity = models.ForeignKey(
        to='activity.Activity',
        on_delete=models.CASCADE)
    profile = models.ForeignKey(
        to='core.Profile',
        on_delete=models.CASCADE)

    # Atividade: v-sne
    (LESS_THAN_15, BETWEEN_15_AND_23, GREATER_THAN_23) = range(0, 3)
    AGE_RANGE_CHOICES = (
        (LESS_THAN_15, _('Menor que 15 anos')),
        (BETWEEN_15_AND_23, _('Entre 15 e 23 anos')),
        (GREATER_THAN_23, _('Maior que 23 anos')),
    )
    age_rage = models.SmallIntegerField(
        _('Sua idade é'), choices=AGE_RANGE_CHOICES,
        null=True, blank=False)
    (PARTNER, ACHIEVER, EX_ACHIEVER, OUTSIDER, VOLUNTEER) = range(0, 5)
    PARTNER_PROFILE_CHOICES = (
        (PARTNER, _('Sócio do Nexa RN')),
        (ACHIEVER, _('Achiever')),
        (EX_ACHIEVER, _('Ex-achiever')),
        (OUTSIDER, _('Externo')),
        (VOLUNTEER, _('Voluntário JARN')),
    )
    partner_profile = models.SmallIntegerField(
        _('Você é...'), choices=PARTNER_PROFILE_CHOICES,
        null=True, blank=False,
        help_text=(
            'Sócio, caso tenha realizado o cadastro; '
            'Achiever, caso esteja participando do programa Miniempresa; '
            'Ex-achiever, caso tenha feito o programa Miniempresa; '
            'Voluntário JARN; '
            'Externo, caso não se aplique aos anteriores.'))
    course = models.CharField(
        _('Em caso de Ensino Superior ou Técnico, qual curso?'),
        max_length=200, null=True, blank=False)
    scholarship_term = models.CharField(
        _('Ano/Período'), help_text=_('Ex.: 3º ano; 6º período'),
        max_length=50, null=True, blank=False)
    (YES, NO) = range(0, 2)
    ALREADY_JOINNED_OUR_PROGRAM_CHOICES = (
        (YES, _('Sim')),
        (NO, _('Não')),
    )
    already_joinned_our_program = models.SmallIntegerField(
        _('Já participou ou participa do programa Miniempresa?'),
        choices=ALREADY_JOINNED_OUR_PROGRAM_CHOICES,
        null=True, blank=False)
    which_one = models.CharField(
        _('Qual Miniempresa? Em qual ano?'),
        max_length=200, null=True, blank=False,
        help_text='(Ex.: BiggLimp S.A./E.; Lumiere S.A/E.; Life tech S.A./E)')
    (YES, NO, ALREADY_KNOWN) = range(0, 3)
    ALREADY_KNOW_US_CHOICES = (
        (YES, _('Sim')),
        (NO, _('Não')),
        (ALREADY_KNOWN, _('Já ouvi falar')),
    )
    already_know_us = models.SmallIntegerField(
        _('Já conhecia o Nexa ou a Junior Achievement?'),
        choices=ALREADY_KNOW_US_CHOICES,
        null=True, blank=False)
    (WHATSAPP, FACEBOOK, TWITTER, BY_MOUHT) = range(0, 4)
    WHERE_KNOW_US_CHOICES = (
        (WHATSAPP, _('WhatsApp')),
        (FACEBOOK, _('Facebook')),
        (TWITTER, _('Twitter')),
        (BY_MOUHT, _('Boca a Boca')),
    )
    where_know_us = models.SmallIntegerField(
        _('Como ficou sabendo do SNE 2015?'),
        choices=WHERE_KNOW_US_CHOICES,
        null=True, blank=False)
    (WHATSAPP, FACEBOOK, TWITTER, BY_MOUHT) = range(0, 4)
    JOIN_PREVIOUS_EDITIONS_CHOICES = (
        (YES, _('Sim')),
        (NO, _('Não')),
    )
    join_previous_editions = models.SmallIntegerField(
        _('Você participou de alguma das edições anteriores do SNE?'),
        choices=JOIN_PREVIOUS_EDITIONS_CHOICES,
        null=True, blank=False)
    which_one = models.CharField(
        _('Quais?'),
        max_length=200, null=True, blank=False,
        help_text=(
            '(Edição I, 2012; Edição II, 2013; '
            'Edição III, 2014; Edição IV 2015)'))

    class Meta:
        verbose_name = _(u'Attendee')
        verbose_name_plural = _(u'Attendees')
        unique_together = ('activity', 'profile')

    def __unicode__(self):
        return u'{0.name}'.format(self)

    @property
    def has_attended(self):
        return True if self.attended_at else False

    @property
    def get_photo_url(self):
        social = self.profile.user.socialaccount_set.first()
        if social:
            return social.get_avatar_url()
        return static('attendee/img/default-profile.png')

    @property
    def get_id_transacao(self):
        return '{0}-{1}'.format(self.code, dateformat(datetime.now(), 'U'))

    def get_absolute_url(self):
        return reverse('attendee:detail', kwargs={
            'activity_slug': self.activity.slug,
            'code': self.code
        })

    def get_send_email_url(self):
        return 'mailto:{.email}'.format(self)

    def get_certificate_url(self, full_url=True):
        url = reverse('attendee:certificate', kwargs={
            'activity_slug': self.activity.slug,
            'code': self.code,
        })
        if full_url:
            return 'http://{domain}{url}'.format(
                domain=Site.objects.get_current().domain, url=url
            )
        else:
            return url

    def get_full_certificate_url(self):
        return self.get_certificate_url(full_url=True)

    def get_payment_url(self, full_url=True):
        url = reverse('attendee:payment', kwargs={
            'activity_slug': self.activity.slug,
            'code': self.code,
        })
        if full_url:
            return 'http://{domain}{url}'.format(
                domain=Site.objects.get_current().domain, url=url
            )
        else:
            return url

    def get_full_payment_url(self):
        return self.get_payment_url(full_url=True)

    def send_welcome_email(self):
        context = {
            'object': self,
            'activity': self.activity,
            'created_by': self.activity.created_by,
        }
        message = render_to_string(
            'mailing/welcome_attendee.txt', context)
        html_message = render_to_string(
            'mailing/welcome_attendee.html', context)
        subject = _(u'Welcome to the "{}"!').format(self.activity.title)
        recipients = [settings.EMAIL_168HORAS, self.email]

        send_mail(
            subject=subject, message=message, html_message=html_message,
            from_email=settings.NO_REPLY_EMAIL, recipient_list=recipients
        )

    def send_pre_sale_welcome_email(self):
        context = {
            'object': self,
            'activity': self.activity,
            'created_by': self.activity.created_by,
        }
        message = render_to_string(
            'mailing/pre_sale_welcome.txt', context)
        html_message = render_to_string(
            'mailing/pre_sale_welcome.html', context)
        subject = _(u'Welcome to the pre-sale of "{}"!').format(
            self.activity.title)
        recipients = [settings.EMAIL_168HORAS, self.email]

        send_mail(
            subject=subject, message=message, html_message=html_message,
            from_email=settings.NO_REPLY_EMAIL, recipient_list=recipients
        )

    def checkin(self):
        if self.attended_at:
            raise ValidationError(_('This Attendee was already checked in.'))
        self.attended_at = datetime.now()
        self.save()

    def uncheck(self):
        if not self.attended_at:
            raise ValidationError(_('This Attendee is not checked in yet.'))
        self.attended_at = None
        self.save()

    def send_payment_confirmation(self):
        context = {
            'object': self,
            'activity': self.activity,
            'created_by': self.activity.created_by,
        }
        message = render_to_string(
            'mailing/payment_confirmation.txt', context)
        html_message = render_to_string(
            'mailing/payment_confirmation.html', context)
        subject = _(u'Payment confirmation of the "{}"!').format(
            self.activity.title)
        recipients = [settings.EMAIL_168HORAS, self.email]

        send_mail(
            subject=subject, message=message, html_message=html_message,
            from_email=settings.NO_REPLY_EMAIL, recipient_list=recipients
        )

        self.activity.notify_payment_organizer(attendee=self)

    def update_payment(self, data):
        if self.moip_status == data.get('status_pagamento'):
            raise ValidationError(
                _('This Attendee was already updated as: {}.').format(
                    self.get_moip_status_display()
                )
            )

        self.moip_status = data.get(
            'status_pagamento', self.moip_status)
        self.moip_payment_type = data.get(
            'tipo_pagamento', self.moip_payment_type)
        self.moip_code = data.get(
            'cod_moip', self.moip_code)
        self.last_updated_at = datetime.now()

        confirmation_status = [
            self.CONCLUIDO, self.AUTORIZADO,
            self.CONFIRMADO_PELO_ORGANIZADOR
        ]
        if self.moip_status in confirmation_status:
            self.status = Attendee.CONFIRMED

        self.save()


def send_attendee_joined_email(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.activity.status == instance.activity.PRE_SALE:
        instance.send_pre_sale_welcome_email()
        instance.activity.notify_pre_sale_organizer(instance)
    else:
        instance.send_welcome_email()


def send_payment_confirmation_email(sender, instance, created, **kwargs):
    if instance.activity.price and instance.status == Attendee.CONFIRMED:
        instance.send_payment_confirmation()


post_save.connect(send_attendee_joined_email, sender=Attendee)
post_save.connect(send_payment_confirmation_email, sender=Attendee)
