from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.contrib import messages

from vanilla import model_views as views
from djqscsv import render_to_csv_response

from core.mixins import PageTitleMixin
from activity.models import Activity
from activity.forms import ActivityForm
from category.views import BaseCategoryView


class BaseActivityView(PageTitleMixin):
    model = Activity
    form_class = ActivityForm
    lookup_field = 'slug'


class ActivityList(BaseCategoryView, views.ListView):
    template_name = 'activity/list.html'
    page_title = _(u'Activities')

    def get_context_data(self, **kwargs):
        context = super(ActivityList, self).get_context_data(**kwargs)
        activities = Activity.objects.filter(
            scheduled_date__gte=timezone.datetime.today().date()
        )
        context.update(
            next_activities=activities.get_next()[:3],
        )
        return context


class ActivityCreate(BaseActivityView, views.CreateView):
    template_name = 'activity/form.html'
    page_title = _(u'Add activity')
    full_page_title = True

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user.profile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ActivityDetail(BaseActivityView, views.DetailView):
    template_name = 'activity/detail.html'
    full_page_title = True


class ActivityUpdate(BaseActivityView, views.UpdateView):
    template_name = 'activity/form.html'


class ActivityDelete(BaseActivityView, views.DeleteView):
    template_name = 'activity/delete.html'

    def get_success_url(self):
        return reverse('activity:list')


class ActivityAttendeeExport(BaseActivityView, views.DetailView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        filename = "%s_attendees" % self.object.slug.replace('-', '_')
        field_header_map = {
            'id': _('Id'),
            'name': _('Name'),
            'cpf': _('CPF'),
            'email': _('Email'),
            'phone': _('Phone'),
            'code': _('Code'),
            'attended_at': _('Attended at'),
        }
        attendees = self.object.attendee_set.values(
            *field_header_map.keys()
        )
        return render_to_csv_response(
            attendees,
            append_datestamp=True,
            filename=filename,
            field_header_map=field_header_map
        )


class ActivityAttendeeCheckAll(BaseActivityView, views.DetailView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            self.object.check_all()
        except ValidationError, e:
            messages.add_message(
                request=self.request, level=messages.ERROR, message=e.message
            )
        else:
            messages.add_message(
                request=self.request, level=messages.SUCCESS,
                message=_(
                    'Successfully checked all the attendees!'
                )
            )
        return redirect(self.object.get_attendee_list_url())


class ActivitySendCertificates(BaseActivityView, views.DetailView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            self.object.send_certificates()
        except ValidationError, e:
            messages.add_message(
                request=self.request, level=messages.ERROR, message=e.message
            )
        else:
            messages.add_message(
                request=self.request, level=messages.SUCCESS,
                message=_(
                    'Successfully sended all the certificates!'
                )
            )
        return redirect(self.object.get_attendee_list_url())
