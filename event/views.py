from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils import timezone

from vanilla import model_views as views

from event.models import Event
from event.forms import EventForm
from category.views import BaseCategoryView
from category.models import Category


class BaseEventView(object):
    model = Event
    form_class = EventForm
    lookup_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(BaseEventView, self).get_context_data(**kwargs)
        if hasattr(self, 'page_title'):
            context.update(page_title=self.page_title)
        return context


class EventByCategoryList(BaseCategoryView, views.ListView):
    template_name = 'event/list_by_category.html'
    queryset = Category.objects.all()
    page_title = _(u'Eventos')

    def get_context_data(self, **kwargs):
        context = super(EventByCategoryList, self).get_context_data(**kwargs)
        events = Event.objects.filter(
            scheduled_date__gte=timezone.datetime.today().date()
        )
        next_events = events.get_next()[:3]
        context.update(
            next_events=next_events,
            events=events,
        )
        return context


class EventList(BaseEventView, views.ListView):
    template_name = 'event/list.html'
    queryset = Event.objects.all()
    page_title = _(u'Maecenas vestibulum')


class EventCreate(BaseEventView, views.CreateView):
    template_name = 'event/form.html'
    page_title = _(u'Adicionar evento')


class EventDetail(BaseEventView, views.DetailView):
    template_name = 'event/detail.html'
    page_title = _(u'Detalhes do evento')


class EventUpdate(BaseEventView, views.UpdateView):
    template_name = 'event/form.html'
    page_title = _(u'Atualizar evento')


class EventDelete(BaseEventView, views.DeleteView):
    template_name = 'event/delete.html'
    page_title = _(u'Remover evento')
    # success_url = reverse('index')

    def get_success_url(self):
        return reverse('event:list')
