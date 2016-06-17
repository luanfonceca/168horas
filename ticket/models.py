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


class Ticket(models.Model):
    name = models.CharField(_('Name'), max_length=200, null=True, blank=True)
    price = models.DecimalField(
        _(u'Price'), max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = CreationDateTimeField(_(u'Created At'))
    available_at = models.DateTimeField(
        _(u'Available At'), null=True, blank=True)
    amount = models.IntegerField(_(u'Amount'), default=20)

    # relations
    activity = models.ForeignKey(
        to='activity.Activity',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = _(u'Ticket')
        verbose_name_plural = _(u'Tickets')

    def __unicode__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse(
            'ticket:list', kwargs={'activity_slug': self.activity.slug})
