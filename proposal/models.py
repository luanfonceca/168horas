# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

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


# class Author(models.Model):
#     name = models.CharField(_('Name'), max_length=300)
#     email = models.EmailField(_('Email'), max_length=300)

#     # relations
#     proposal = models.ForeignKey(
#         to='proposal.Proposal',
#         on_delete=models.CASCADE,
#         related_name='authors'
#     )

#     class Meta:
#         verbose_name = _('Author')
#         verbose_name_plural = _('Author')
#         ordering = ('-created_at',)
