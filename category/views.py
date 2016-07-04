from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vanilla import model_views as views
from djqscsv import render_to_csv_response

from core.mixins import PageTitleMixin
from category.models import Category
from category.forms import CategoryForm
from attendee.models import Attendee


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
            'id': _('Id'),
            'first_name': _('First Name'),
            'name': _('Name'),
            'cpf': _('CPF'),
            'email': _('Email Address'),
            'phone': _('Phone'),
            'code': _('Code'),
            'attended_at': _('Attended at'),
        }

        attendees = Attendee.objects.filter(
            activity__in=self.object.activities.all()
        ).extra(
            select={'first_name': "split_part(name, ' ', 1)"}
        ).values(
            *field_header_map.keys()
        )
        return render_to_csv_response(
            attendees,
            append_datestamp=True,
            filename=filename,
            field_header_map=field_header_map
        )
