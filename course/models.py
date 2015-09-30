from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from django_extensions.db.fields import CreationDateTimeField
from django_extensions.db.models import TitleSlugDescriptionModel


class CouseManager(models.QuerySet):
    def is_public(self):
        return self.filter(is_public=True)


class Course(TitleSlugDescriptionModel):
    created_at = CreationDateTimeField(_(u'Created At'))
    is_published = models.BooleanField(_(u'Is Published'), default=True)
    is_public = models.BooleanField(_(u'Is Public'), default=True)

    # managers
    objects = CouseManager.as_manager()

    class Meta:
        verbose_name = _(u'Course')
        verbose_name_plural = _(u'Courses')

    def __str__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        return reverse('course:detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('course:update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('course:delete', kwargs={'slug': self.slug})
