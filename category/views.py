from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vanilla import model_views as views

from core.views import PageTitleView
from category.models import Category
from category.forms import CategoryForm


class BaseCategoryView(PageTitleView):
    model = Category
    form_class = CategoryForm
    lookup_field = 'slug'


class CategoryList(BaseCategoryView, views.ListView):
    template_name = 'category/list.html'
    queryset = Category.objects.all()
    page_title = _(u'Eventos')


class CategoryCreate(BaseCategoryView, views.CreateView):
    template_name = 'category/form.html'
    # page_title = _(u'Aenean vulputate eleifend')


class CategoryDetail(BaseCategoryView, views.DetailView):
    template_name = 'category/detail.html'
    # page_title = _(u'Eventos desta categoria')


class CategoryUpdate(BaseCategoryView, views.UpdateView):
    template_name = 'category/form.html'
    # page_title = _(u'Fusce ac felis')


class CategoryDelete(BaseCategoryView, views.DeleteView):
    template_name = 'category/delete.html'
    # page_title = _(u'Fusce ac felis')
    # success_url = reverse('index')

    def get_success_url(self):
        return reverse('category:list')
