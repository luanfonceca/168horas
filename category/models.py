from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _


from django_extensions.db.models import TitleSlugDescriptionModel


class Category(TitleSlugDescriptionModel):
    class Meta:
        verbose_name = _(u'Category')
        verbose_name_plural = _(u'Categories')

    def __str__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        return reverse('category:detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('category:update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('category:delete', kwargs={'slug': self.slug})
