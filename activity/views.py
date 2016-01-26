from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.utils import timezone

from vanilla import model_views as views

from core.mixins import PageTitleMixin
from activity.models import Activity
from activity.forms import ActivityForm
from category.views import BaseCategoryView
from category.models import Category


class BaseActivityView(PageTitleMixin):
    model = Activity
    form_class = ActivityForm
    lookup_field = 'slug'


class ActivityList(BaseCategoryView, views.ListView):
    template_name = 'activity/list_by_category.html'
    queryset = Category.objects.all()
    page_title = _(u'Activities')

    def get_context_data(self, **kwargs):
        context = super(ActivityList, self).get_context_data(**kwargs)
        activities = Activity.objects.filter(
            scheduled_date__gte=timezone.datetime.today().date()
        )
        next_activities = activities.get_next()[:3]
        context.update(
            next_activities=next_activities,
            activities=activities,
        )
        return context


class ActivityCreate(BaseActivityView, views.CreateView):
    template_name = 'activity/form.html'
    page_title = _(u'Add activity')

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user.profile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ActivityDetail(BaseActivityView, views.DetailView):
    template_name = 'activity/detail.html'


class ActivityUpdate(BaseActivityView, views.UpdateView):
    template_name = 'activity/form.html'


class ActivityDelete(BaseActivityView, views.DeleteView):
    template_name = 'activity/delete.html'

    def get_success_url(self):
        return reverse('activity:list')
