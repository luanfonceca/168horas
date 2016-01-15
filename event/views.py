from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.utils import timezone

from vanilla import model_views as views

from core.mixins import PageTitleMixin
from event.models import Event
from event.forms import EventForm
from category.views import BaseCategoryView
from category.models import Category


class BaseEventView(PageTitleMixin):
    model = Event
    form_class = EventForm
    lookup_field = 'slug'


class EventList(BaseCategoryView, views.ListView):
    template_name = 'event/list_by_category.html'
    queryset = Category.objects.all()
    page_title = _(u'Eventos')

    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        events = Event.objects.filter(
            scheduled_date__gte=timezone.datetime.today().date()
        )
        next_events = events.get_next()[:3]
        context.update(
            next_events=next_events,
            events=events,
        )
        return context


class EventCreate(BaseEventView, views.CreateView):
    template_name = 'event/form.html'
    page_title = _(u'Adicionar evento')

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user.profile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class EventDetail(BaseEventView, views.DetailView):
    template_name = 'event/detail.html'


class EventUpdate(BaseEventView, views.UpdateView):
    template_name = 'event/form.html'


class EventDelete(BaseEventView, views.DeleteView):
    template_name = 'event/delete.html'

    def get_success_url(self):
        return reverse('event:list')
