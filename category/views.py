from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vanilla import model_views as views

from event.models import Event
from category.models import Category
from category.forms import CategoryForm


class BaseCategoryView(object):
    model = Category
    form_class = CategoryForm
    lookup_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(BaseCategoryView, self).get_context_data(**kwargs)
        if hasattr(self, 'page_title'):
            context.update(page_title=self.page_title)
        return context


class EventByCategoryList(BaseCategoryView, views.ListView):
    template_name = 'category/list_events_by_category.html'
    queryset = Category.objects.all()
    page_title = _(u'Eventos')

    def get_context_data(self, **kwargs):
        context = super(EventByCategoryList, self).get_context_data(**kwargs)
        next_events = Event.objects.get_next()[:3]
        context.update(next_events=next_events)
        return context


class CategoryList(BaseCategoryView, views.ListView):
    template_name = 'category/list.html'
    queryset = Category.objects.all()
    page_title = _(u'Maecenas vestibulum')


class CategoryCreate(BaseCategoryView, views.CreateView):
    template_name = 'category/form.html'
    page_title = _(u'Aenean vulputate eleifend')


class CategoryDetail(BaseCategoryView, views.DetailView):
    template_name = 'category/detail.html'
    page_title = _(u'Eventos desta categoria')


class CategoryUpdate(BaseCategoryView, views.UpdateView):
    template_name = 'category/form.html'
    page_title = _(u'Fusce ac felis')


class CategoryDelete(BaseCategoryView, views.DeleteView):
    template_name = 'category/delete.html'
    page_title = _(u'Fusce ac felis')
    # success_url = reverse('index')

    def get_success_url(self):
        return reverse('category:list')
