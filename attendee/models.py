import random
import string

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.db import models

from django_extensions.db.fields import CreationDateTimeField


def code_generate(size=10):
    return ''.join(
        random.choice(
            string.ascii_uppercase + string.digits
        ) for x in range(size))


class Attendee(models.Model):
    name = models.CharField(_('Name'), max_length=200, null=True, blank=True)
    cpf = models.CharField('CPF', max_length=14, null=True, blank=True)
    email = models.EmailField(_('Email'), null=True, blank=True)
    phone = models.CharField(_('Phone'), max_length=50, blank=True)
    code = models.CharField(_('Code'), max_length=10, default=code_generate())
    created_at = CreationDateTimeField(_(u'Created At'))
    attended_at = models.DateTimeField(
        _(u'Attended At'), null=True, blank=True)

    # relations
    activity = models.ForeignKey(
        to='activity.Activity',
        on_delete=models.CASCADE)
    profile = models.ForeignKey(
        to='core.Profile',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = _(u'Attendee')
        verbose_name_plural = _(u'Attendees')
        unique_together = ('activity', 'profile')

    def __unicode__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse(
            'attendee:list', kwargs={'activity_slug': self.activity.slug})

    def get_send_email_url(self):
        return 'mailto:{.profile.user.email}'.format(self)

    @property
    def has_attended(self):
        return True if self.attended_at else False

    @property
    def get_photo_url(self):
        social = self.profile.user.socialaccount_set.first()
        if social:
            return social.get_avatar_url()
