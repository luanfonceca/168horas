from django.db import models
from django.conf import settings
from django.core.exceptions import AppRegistryNotReady
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse_lazy

from localflavor.br import br_states


class Profile(models.Model):
    state = models.CharField(
        'State', max_length=50, choices=br_states.STATE_CHOICES)
    cpf = models.CharField('CPF', max_length=14, null=True, blank=True)
    cnpj = models.CharField('CPF', max_length=18, null=True, blank=True)
    digital_signature = models.ImageField(
        upload_to='signatures/', null=True, blank=True,
        help_text='PNG signatures in the resolution: 200x200.')
    organizer_name = models.CharField(max_length=200, null=True, blank=True)

    # relations
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL, null=True, blank=True)
    categories = models.ManyToManyField(to='category.Category')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse_lazy('profile')

    @property
    def ident(self):
        return self.cpf or self.cnpj


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except AppRegistryNotReady:
    from django.contrib.auth.models import User

post_save.connect(create_user_profile, sender=User)
