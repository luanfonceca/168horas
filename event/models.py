from django.db import models
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils.timezone import datetime

from PIL import Image

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
        help_text='Images in the resolution: 400x400.')
    location = models.CharField(
        _(u'Location'), max_length=500, null=True, blank=True)
    is_online = models.BooleanField(default=False)

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


def resize_event_photo(sender, instance, **kwargs):
    try:
        image = Image.open(instance.photo.path)
    except ValueError:
        return

    if (image.width, image.height) == (400, 400):
        return

    image = image.resize((400, 400), Image.ANTIALIAS)
    image.save(instance.photo.path, quality=90)

post_save.connect(resize_event_photo, sender=Event)
