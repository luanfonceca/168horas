from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from vanilla import model_views as views
from easy_pdf.views import PDFTemplateResponseMixin

from core.mixins import PageTitleMixin, LoginRequiredMixin
from activity.models import Activity
from attendee.models import Attendee
from attendee.forms import (
    AttendeeForm, AttendeePaymentForm)


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
    paginate_by = 30
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super(AttendeeList, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        # paginator = self.get_paginator(queryset, self.paginate_by)
        # pagination = paginator.page(self.request.GET.get('page', 1))

        context.update(
            search=self.request.GET.get('search'),
            # pagination=pagination,
            total_count=queryset.count(),
        )
        return context

    def get_queryset(self):
        queryset = super(AttendeeList, self).get_queryset()

        self.activity = self.get_activity()
        if self.activity.price:
            queryset = queryset.filter(payment_status=Attendee.COMPLETE)

        queryset = queryset.filter(activity=self.get_activity())

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search) |
                Q(cpf__icontains=search) |
                Q(code__icontains=search)
            )
        return queryset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.activity = self.get_activity()
        if self.request.user.profile != self.activity.created_by and \
           not self.request.user.is_superuser:
            messages.add_message(
                request=self.request, level=messages.ERROR,
                message=_('You are not allowed to see this page!')
            )
            return redirect(self.activity)
        return super(AttendeeList, self).dispatch(*args, **kwargs)


class AttendeeJoin(BaseAttendeeView, LoginRequiredMixin, views.CreateView):
    template_name = 'attendee/form.html'
    full_page_title = True

    def get_page_title(self):
        activity = self.get_activity()
        return _(u'Join to {activity}').format(activity=activity)

    def get_context_data(self, **kwargs):
        context = super(AttendeeJoin, self).get_context_data(**kwargs)
        context.update(
            activity=self.get_activity(),
            required_attendee_fields=['name', 'email', 'cpf', 'phone'],
        )
        return context

    def get(self, request, *args, **kwargs):
        already_joined = Attendee.objects.filter(
            profile=self.request.user.profile,
            activity=self.get_activity(),
        ).exists()

        if already_joined:
            messages.add_message(
                request=self.request, level=messages.SUCCESS,
                message=_('You already joined up for this activity!')
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
                message=_('This user already joined up for this activity!')
            )
            return redirect(self.activity.get_attendee_join_url())
        else:
            messages.add_message(
                request=self.request, level=messages.SUCCESS,
                message=_('Successfully joined up for this activity!')
            )
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        self.activity = self.get_activity()
        if self.activity.price:
            return self.activity.get_attendee_payment_url()
        elif self.activity.created_by != self.request.user.profile:
            return self.activity.get_absolute_url()
        elif self.activity.price:
            return self.activity.get_attendee_payment_url()
        return super(AttendeeJoin, self).get_success_url()


class AttendeePayment(BaseAttendeeView,
                      LoginRequiredMixin,
                      views.DetailView):
    template_name = 'attendee/form_payment.html'
    form_class = AttendeePaymentForm

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AttendeePayment, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AttendeePayment, self).get_context_data(**kwargs)
        context.update(form=self.get_form())
        return context

    def get_object(self):
        return Attendee.objects.get(
            profile=self.request.user.profile,
            activity=self.get_activity(),
        )

    def get_page_title(self):
        activity = self.get_activity()
        return _(u'Payment for {activity}').format(activity=activity)

    def get_form(self, data=None, files=None, **kwargs):
        domain = Site.objects.get_current().domain
        self.activity = self.get_activity()
        self.object = self.get_object()

        notify_url = 'http://{domain}{url}'.format(
            domain=domain, url=reverse('paypal-ipn'))
        return_url = self.activity.get_full_attendee_payment_url()

        kwargs.update(initial={
            'business': 'luanfonceca@gmail.com',
            'currency_code': 'BRL',
            'amount': self.activity.price,
            'item_name': 'Ticket for "{0}"'.format(self.activity),
            'invoice': 'invoice-{0}-{1}'.format(
                self.activity.slug, self.object.code
            ),
            'notify_url': notify_url,
            'return_url': return_url,
            'cancel_return': return_url,
            # 'custom': 'Upgrade all users!',
        })
        return super(AttendeePayment, self).get_form(
            data=data, files=files, **kwargs
        )

    def post(self, request, *args, **kwargs):
        activity = self.get_activity()
        message = _('Payment Successfully charged.')
        messages.add_message(
            request=self.request, level=messages.ERROR, message=message
        )
        return redirect(activity.get_absolute_url())


class AttendeeCheck(BaseAttendeeView, views.UpdateView):
    lookup_field = 'code'

    def post(self, request, *args, **kwargs):
        self.activity = self.get_activity()
        self.object = self.get_object()

        try:
            self.object.checkin()
        except ValidationError, e:
            messages.add_message(
                request=self.request, level=messages.ERROR, message=e.message
            )
        else:
            messages.add_message(
                request=self.request, level=messages.SUCCESS,
                message=_(
                    'Successfully checked in the attendee "{0}"!'
                ).format(self.object)
            )
        return redirect(self.activity.get_attendee_list_url())


class AttendeeUncheck(BaseAttendeeView, views.UpdateView):
    lookup_field = 'code'

    def post(self, request, *args, **kwargs):
        self.activity = self.get_activity()
        self.object = self.get_object()

        try:
            self.object.uncheck()
        except ValidationError, e:
            messages.add_message(
                request=self.request, level=messages.ERROR, message=e.message
            )
        else:
            messages.add_message(
                request=self.request, level=messages.SUCCESS,
                message=_(
                    'Successfully unchecked the attendee "{0}"!'
                ).format(self.object)
            )
        return redirect(self.activity.get_attendee_list_url())


class AttendeeCertificate(BaseAttendeeView,
                          PDFTemplateResponseMixin,
                          views.DetailView):
    lookup_field = 'code'
    template_name = 'attendee/certificate.html'
    page_title = _('Certificate')


class AttendeeSort(BaseAttendeeView,
                   views.DetailView):
    lookup_field = 'code'
    template_name = 'attendee/sort.html'
    page_title = _('Sort')

    def get_object(self):
        queryset = self.get_queryset()
        return queryset.filter(attended_at__isnull=False).order_by('?').first()
