from django.db import models
from django.conf import settings
from django.core.exceptions import AppRegistryNotReady
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _

from localflavor.br import br_states

import analytics
analytics.write_key = settings.SEGMENT_KEY


class Profile(models.Model):
    state = models.CharField(
        _('State'), max_length=50, choices=br_states.STATE_CHOICES)
    cpf = models.CharField(_('CPF'), max_length=14, null=True, blank=True)
    cnpj = models.CharField(_('CNPJ'), max_length=18, null=True, blank=True)
    digital_signature = models.ImageField(
        _('Digital Signature'),
        upload_to='signatures/', null=True, blank=True,
        help_text=_('PNG signatures in the resolution: 200x200.'))
    organizer_name = models.CharField(
        _('Organizer Name'), max_length=200, null=True, blank=True)
    organizer_email = models.EmailField(
        _('Organizer Email'), max_length=200, null=True, blank=True)
    organizer_phone = models.CharField(
        _('Organizer Phone'), max_length=30, null=True, blank=True)

    # relations
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL, null=True, blank=True)
    categories = models.ManyToManyField(
        to='category.Category', verbose_name=_('Categories'))

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse_lazy('profile')

    @property
    def ident(self):
        return self.cpf or self.cnpj

    def is_organizer(self, activty):
        return activty.organizers.filter(pk=self.pk).exists()


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def create_segment_refrence(sender, instance, created, **kwargs):
    user = instance.user
    if created:
        analytics.identify(user.id, {
            'name': user.get_full_name(),
            'email': user.email,
            'created_at': user.created_at
        })

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except AppRegistryNotReady:
    from django.contrib.auth.models import User

post_save.connect(create_user_profile, sender=User)
post_save.connect(create_segment_refrence, sender=User)
