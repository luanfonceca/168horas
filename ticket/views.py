from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from vanilla import model_views as views

from core.mixins import PageTitleMixin
from ticket.models import Ticket
from ticket.forms import TicketForm
# from category.views import BaseCategoryView
from activity.models import Activity


class BaseTicketView(PageTitleMixin):
    model = Ticket
    form_class = TicketForm
    lookup_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(BaseTicketView, self).get_context_data(**kwargs)
        context.update(activity=self.get_activity())
        return context

    def get_activity(self):
        return get_object_or_404(
            Activity,
            slug=self.kwargs.get('activity_slug'))


class TicketList(BaseTicketView, views.ListView):
    template_name = 'ticket/list.html'

    def get_queryset(self):
        queryset = super(TicketList, self).get_queryset()
        queryset = queryset.filter(activity=self.get_activity())
        return queryset


class TicketCreate(BaseTicketView, views.CreateView):
    template_name = 'ticket/form.html'
    page_title = _(u'Add ticket')

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user.profile
        self.object.activity = self.get_activity()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class TicketDetail(BaseTicketView, views.DetailView):
    template_name = 'ticket/detail.html'


class TicketUpdate(BaseTicketView, views.UpdateView):
    template_name = 'ticket/form.html'


class TicketDelete(BaseTicketView, views.DeleteView):
    template_name = 'ticket/delete.html'

    def get_success_url(self):
        return reverse('ticket:list')
