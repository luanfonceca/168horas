from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vanilla import model_views as views

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
