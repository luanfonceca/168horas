from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _


from django_extensions.db.models import TitleSlugDescriptionModel


class Category(TitleSlugDescriptionModel):
    class Meta:
        verbose_name = _(u'Category')
        verbose_name_plural = _(u'Categories')
        ordering = ('title',)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category:detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('category:update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('category:delete', kwargs={'slug': self.slug})

    def get_export_attendees_url(self):
        return reverse('category:export_attendees', kwargs={'slug': self.slug})
