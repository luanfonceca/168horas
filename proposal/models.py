# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from django_extensions.db.fields import CreationDateTimeField, AutoSlugField


class Proposal(models.Model):
    CODIGOS_E_LINGUAGENS = 'codigos-e-linguagens'
    CIENCIAS_DA_NATUREZA_E_SUAS_TECNOLOGIAS = \
        'ciencias-da-natureza-e-suas-tecnologias'
    ELETRONICA = 'eletronica'
    GESTAO_E_NEGOCIOS = 'gestao-e-negocios'
    INFORMATICA = 'informatica'
    MARKETING = 'marketing'
    EDUCACAO = 'educacao'

    AREA_CHOICES = (
        (CODIGOS_E_LINGUAGENS, _('Códigos e Linguagenns')),
        (CIENCIAS_DA_NATUREZA_E_SUAS_TECNOLOGIAS,
            _('Ciências da Natureza e Suas Tecnologias')),
        (ELETRONICA, _('Eletrônica')),
        (GESTAO_E_NEGOCIOS, _('Gestão e Negócios')),
        (INFORMATICA, _('Informática')),
        (MARKETING, _('Marketing')),
        (EDUCACAO, _('Educação')),
    )

    title = models.CharField(_('Title'), max_length=300)
    slug = AutoSlugField(
        populate_from='title', overwrite=True,
        max_length=340, unique=True, db_index=True)
    brief = models.TextField(
        _('Brief'), max_length=1000, blank=True,
        help_text=_('Max of 300 words.'))
    created_at = CreationDateTimeField(_(u'Created At'))
    area = models.CharField(
        _('Area'), choices=AREA_CHOICES, max_length=100)
    document = models.FileField(_('Document'), null=True, blank=True)

    # relations
    activity = models.ForeignKey(
        to='activity.Activity',
        on_delete=models.CASCADE,
        related_name='proposals')
    created_by = models.ForeignKey(
        to='core.Profile',
        on_delete=models.CASCADE,
        related_name='proposals')

    # SIPEX - Minicursos
    (DUAS_HORAS, QUATRO_HORAS, SEIS_HORAS) = range(3)
    CARGA_HORARIA_CHOICES = (
        (DUAS_HORAS, _('Duas Horas')),
        (QUATRO_HORAS, _('Quatro Horas')),
        (SEIS_HORAS, _('Seis Horas')),
    )

    (DUAS_HORAS, QUATRO_HORAS, SEIS_HORAS) = range(3)
    PUBLICO_CHOICES = (
        (DUAS_HORAS, _('Duas Horas')),
        (QUATRO_HORAS, _('Quatro Horas')),
        (SEIS_HORAS, _('Seis Horas')),
    )

    carga_horaria = models.IntegerField(
        _('Carga horária'), choices=CARGA_HORARIA_CHOICES, default=DUAS_HORAS,
        null=True, blank=True)
    quantidade_de_vagas = models.IntegerField(
        _('Quantidade de Vagas'), null=True, blank=False)
    institution = models.CharField(
        _('Institution'), max_length=200, null=True, blank=False)
    ementa = models.TextField(
        _('Ementa'), max_length=1000, blank=False)
    objetivos = models.TextField(
        _('Objetivos'), max_length=1000, blank=False)
    publico = models.CharField(
        _('Tipo de Público'), max_length=300, null=True, blank=False)
    materiais = models.TextField(
        _('Materiais necessários'), max_length=1000, blank=False)
    justificativa = models.TextField(
        _('Justificativa'), max_length=1000, blank=False)
    pre_requisitos = models.TextField(
        _('Pré-requisitos'), max_length=2000,
        null=True, blank=False)

    class Meta:
        verbose_name = _('Proposal')
        verbose_name_plural = _('Proposals')
        ordering = ('-created_at',)

    def __unicode__(self):
        return u'{0.title}'.format(self)

    def get_absolute_url(self):
        return reverse('proposal:detail', kwargs={
            'activity_slug': self.activity.slug,
            'slug': self.slug
        })

    def get_update_url(self):
        return reverse('proposal:update', kwargs={
            'activity_slug': self.activity.slug,
            'slug': self.slug
        })

    def get_delete_url(self):
        return reverse('proposal:delete', kwargs={
            'activity_slug': self.activity.slug,
            'slug': self.slug
        })

    def get_authors_email(self):
        return self.authors.values('email', flat=True)

    def send_submited_proposal_email(self):
        context = {
            'proposal': self,
            'activity': self.activity,
        }
        message = render_to_string(
            'mailing/submited_proposal.txt', context)
        html_message = render_to_string(
            'mailing/submited_proposal.html', context)
        subject = _(u'Submited Proposal to the "{}"!').format(
            self.activity.title)
        recipients = [
            settings.EMAIL_168HORAS,
            self.created_by.user.email,
            self.activity.created_by.user.email
        ]

        send_mail(
            subject=subject, message=message, html_message=html_message,
            from_email=settings.NO_REPLY_EMAIL, recipient_list=recipients
        )


class Author(models.Model):
    name = models.CharField(_('Name'), max_length=300)
    email = models.EmailField(_('Email'), max_length=300)

    # relations
    proposal = models.ForeignKey(
        to='proposal.Proposal',
        on_delete=models.CASCADE,
        related_name='authors'
    )

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Author')

    def send_submited_proposal_email(self):
        context = {
            'proposal': self.proposal,
            'activity': self.proposal.activity,
        }
        message = render_to_string(
            'mailing/submited_proposal.txt', context)
        html_message = render_to_string(
            'mailing/submited_proposal.html', context)
        subject = _(u'Submited Proposal to the "{}"!').format(
            self.proposal.activity.title)
        recipients = [
            settings.EMAIL_168HORAS,
            self.email,
        ]

        send_mail(
            subject=subject, message=message, html_message=html_message,
            from_email=settings.NO_REPLY_EMAIL, recipient_list=recipients
        )


def send_proposal_submited_email(sender, instance, created, **kwargs):
    if not created:
        return

    instance.send_submited_proposal_email()


post_save.connect(send_proposal_submited_email, sender=Proposal)
post_save.connect(send_proposal_submited_email, sender=Author)
