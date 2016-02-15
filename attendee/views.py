from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect


from vanilla import model_views as views
from djqscsv import render_to_csv_response

from core.mixins import PageTitleMixin
from activity.models import Activity
from attendee.models import Attendee
from attendee.forms import AttendeeForm


class BaseAttendeeView(PageTitleMixin):
    model = Attendee
    form_class = AttendeeForm
    lookup_field = 'activity_slug'

    def get_context_data(self, **kwargs):
        context = super(BaseAttendeeView, self).get_context_data(**kwargs)
        context.update(activity=self.get_activity())
        return context

    def get_activity(self):
        return get_object_or_404(
            Activity,
            slug=self.kwargs.get('activity_slug'))


class AttendeeList(BaseAttendeeView, views.ListView):
    template_name = 'attendee/list.html'
    page_title = _(u'Attendees')

    def get_queryset(self):
        queryset = super(AttendeeList, self).get_queryset()
        queryset = queryset.filter(activity=self.get_activity())
        return queryset


class AttendeeJoin(BaseAttendeeView, views.CreateView):
    template_name = 'attendee/form.html'

    def get_page_title(self):
        activity = self.get_activity()
        return _(u'Join to {activity}').format(activity=activity)

    def get(self, request, *args, **kwargs):
        already_joined = Attendee.objects.filter(
            profile=self.request.user.profile,
            activity=self.get_activity(),
        ).exists()

        if already_joined:
            messages.add_message(
                request=self.request, level=messages.SUCCESS,
                message=_('You already joined up for this event!')
            )

        return super(AttendeeJoin, self).get(request, *args, **kwargs)

    def get_form(self, data=None, files=None, **kwargs):
        kwargs.update(initial={
            'name': self.request.user.get_full_name(),
            'email': self.request.user.email,
        })
        return super(AttendeeJoin, self).get_form(
            data=data, files=files, **kwargs
        )

    def form_valid(self, form):
        self.activity = self.get_activity()
        self.object = form.save(commit=False)
        self.object.profile = self.request.user.profile
        self.object.activity = self.activity

        try:
            self.object.save()
        except IntegrityError:
            messages.add_message(
                request=self.request, level=messages.ERROR,
                message=_('This user already joined up for this event!')
            )
            return redirect(self.activity.get_attendee_join_url())
        else:
            return HttpResponseRedirect(self.get_success_url())


class ExportAttendeeList(BaseAttendeeView, views.DetailView):
    def get(self, request, *args, **kwargs):
        activity = self.get_activity()
        filename = "%s_attendees" % activity.slug.replace('-', '_')
        field_header_map = {
            'id': _('Id'),
            'name': _('Name'),
            'cpf': _('CPF'),
            'email': _('Email'),
            'phone': _('Phone'),
            'code': _('Code'),
            'attended_at': _('Attended at'),
        }
        attendees = activity.attendee_set.values(
            *field_header_map.keys()
        )
        return render_to_csv_response(
            attendees,
            append_datestamp=True,
            filename=filename,
            field_header_map=field_header_map
        )
