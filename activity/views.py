from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.contrib import messages

from vanilla import model_views as views
from djqscsv import render_to_csv_response

from core.mixins import (
    PageTitleMixin, BreadcrumbMixin,
    OrganizerRequiredMixin,
)
from activity.models import Activity
from activity.forms import ActivityForm
from category.views import BaseCategoryView
from attendee.models import Attendee


def _get_display(data, field_name):
    field = Attendee._meta.get_field(field_name)
    value = data.get(field_name)
    return dict(field.flatchoices).get(value, value)


def update_display(attendee):
    attendee.update(
        status=_get_display(attendee, 'status'),
        moip_status=_get_display(
            attendee, 'moip_status'),
        moip_payment_type=_get_display(
            attendee, 'moip_payment_type')
    )


def update_display_v_sne(attendee):
    attendee.update(
        age_rage=_get_display(attendee, 'age_rage'),
        partner_profile=_get_display(attendee, 'partner_profile'),
    )


class BaseActivityView(PageTitleMixin, BreadcrumbMixin):
    model = Activity
    form_class = ActivityForm
    lookup_field = 'slug'


class ActivityList(BaseCategoryView, views.ListView):
    template_name = 'activity/list.html'
    page_title = _(u'Activities')

    def get_context_data(self, **kwargs):
        context = super(ActivityList, self).get_context_data(**kwargs)
        activities = Activity.objects.is_public().filter(
            scheduled_date__gte=timezone.datetime.today().date(),
        )
        context.update(
            next_activities=activities.get_next()[:3],
        )
        return context


class ActivityCreate(BaseActivityView, views.CreateView):
    template_name = 'activity/form.html'
    page_title = _(u'Create')
    full_page_title = True

    def get_breadcrumbs(self):
        return [{
            'url': reverse('activity:list'),
            'title': _('Activities')
        }, {
            'url': reverse('activity:create'),
            'title': self.get_page_title()
        }]

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user.profile
        self.object.save()

        self.object.organizers.add(self.object.created_by)
        return HttpResponseRedirect(self.get_success_url())


class ActivityDetail(BaseActivityView, views.DetailView):
    template_name = 'activity/detail.html'
    full_page_title = True


class ActivityDetailShortUrl(BaseActivityView, views.DetailView):
    lookup_field = 'short_url'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return redirect(self.object.get_absolute_url())


class ActivityUpdate(BaseActivityView,
                     OrganizerRequiredMixin,
                     views.UpdateView):
    template_name = 'activity/form.html'
    full_page_title = True

    def get_error_redirect_url(self):
        self.object = self.get_object()
        return self.object.get_absolute_url()

    def get_breadcrumbs(self):
        self.object = self.get_object()

        return [{
            'url': self.object.get_absolute_url(),
            'title': self.object.title
        }, {
            'url': self.object.get_update_url(),
            'title': _('Update')
        }]


class ActivityDelete(BaseActivityView,
                     OrganizerRequiredMixin,
                     views.DeleteView):
    template_name = 'activity/delete.html'
    full_page_title = True

    def get_breadcrumbs(self):
        self.object = self.get_object()

        return [{
            'url': self.object.get_absolute_url(),
            'title': self.object.title
        }, {
            'url': self.object.get_delete_url(),
            'title': _('Delete')
        }]

    def get_success_url(self):
        return reverse('activity:list')


class ActivityAttendeeExport(BaseActivityView,
                             OrganizerRequiredMixin,
                             views.DetailView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        filename = "%s_attendees" % self.object.slug.replace('-', '_')
        field_header_map = {
            'id': _('Id'),
            'first_name': _('First Name'),
            'name': _('Name'),
            'cpf': _('CPF'),
            'email': _('Email Address'),
            'phone': _('Phone'),
            'code': _('Code'),
            'attended_at': _('Attended at'),
        }

        if self.object.price:
            field_header_map.update({
                'status': _('Subscription status'),
                'moip_status': _('Payment status'),
                'moip_payment_type': _('Payment type'),
            })

        v_sne_slug = 'v-simposio-nexa-de-empreendedorismo-construindo-op'
        if self.object.slug == v_sne_slug:
            field_header_map.update({
                'age_rage': _('Idade'),
                'partner_profile': _('Eu sou'),
            })

        attendees = self.object.attendee_set.extra(
            select={'first_name': "split_part(name, ' ', 1)"}
        ).values(
            *field_header_map.keys()
        ).order_by('name')

        if self.object.price:
            map((lambda a: update_display(a)), attendees)

        if self.object.slug == v_sne_slug:
            map((lambda a: update_display_v_sne(a)), attendees)

        return render_to_csv_response(
            attendees,
            append_datestamp=True,
            filename=filename,
            field_header_map=field_header_map
        )


class ActivityAttendeeCheckAll(BaseActivityView,
                               OrganizerRequiredMixin,
                               views.DetailView):
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


class ActivitySendCertificates(BaseActivityView,
                               OrganizerRequiredMixin,
                               views.DetailView):
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
