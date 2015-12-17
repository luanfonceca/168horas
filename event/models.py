from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils.timezone import datetime

from web168h import settings

from django_extensions.db.fields import CreationDateTimeField
from django_extensions.db.models import TitleSlugDescriptionModel


class CouseManager(models.QuerySet):
    def is_public(self):
        return self.filter(is_public=True)

    def get_next(self):
        return self.filter(
            models.Q(scheduled_date__isnull=True) |
            models.Q(scheduled_date__gte=datetime.today())
        ).extra(
            select=dict(date_is_null='scheduled_date IS NULL'),
            order_by=['date_is_null', 'scheduled_date'],
        )


class Event(TitleSlugDescriptionModel):
    link = models.URLField(_(u'Link'), max_length=300, null=True, blank=True)
    scheduled_date = models.DateField(_(u'Data'), null=True, blank=True)
    created_at = CreationDateTimeField(_(u'Created At'))
    is_published = models.BooleanField(_(u'Is Published'), default=True)
    is_public = models.BooleanField(_(u'Is Public'), default=True)
    photo = models.ImageField(
        upload_to='photos/', null=True, blank=True,
        help_text='Images in the resolution: 300x300.')

    # relations
    categories = models.ManyToManyField(
        verbose_name=_(u'Categorias'),
        to='category.Category',
        related_name='events')

    # managers
    objects = CouseManager.as_manager()

    class Meta:
        verbose_name = _(u'Event')
        verbose_name_plural = _(u'Events')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event:detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('event:update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('event:delete', kwargs={'slug': self.slug})

    @property
    def get_photo_url(self):
        return '{0}/{1}'.format(settings.MEDIA_URL, self.photo)
