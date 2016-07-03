from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vanilla import model_views as views
from djqscsv import render_to_csv_response

from core.mixins import PageTitleMixin
from category.models import Category
from category.forms import CategoryForm


class BaseCategoryView(PageTitleMixin):
    model = Category
    form_class = CategoryForm
    lookup_field = 'slug'


class CategoryList(BaseCategoryView, views.ListView):
    template_name = 'category/list.html'
    page_title = _(u'Categorias')


class CategoryCreate(BaseCategoryView, views.CreateView):
    template_name = 'category/form.html'


class CategoryDetail(BaseCategoryView, views.DetailView):
    template_name = 'category/detail.html'


class CategoryUpdate(BaseCategoryView, views.UpdateView):
    template_name = 'category/form.html'


class CategoryDelete(BaseCategoryView, views.DeleteView):
    template_name = 'category/delete.html'

    def get_success_url(self):
        return reverse('category:list')


class CategoryAttendeeExport(BaseCategoryView, views.DetailView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        filename = "%s_attendees" % self.object.slug.replace('-', '_')
        field_header_map = {
            'title': _('Activity'),
            'attendee__id': _('Id'),
            'attendee__name': _('Name'),
            'attendee__cpf': _('CPF'),
            'attendee__email': _('Email'),
            'attendee__phone': _('Phone'),
            'attendee__code': _('Code'),
            'attendee__attended_at': _('Attended at'),
        }

        attendees = self.object.activities.values(
            *field_header_map.keys()
        ).distinct()

        return render_to_csv_response(
            attendees,
            append_datestamp=True,
            filename=filename,
            field_header_map=field_header_map
        )
