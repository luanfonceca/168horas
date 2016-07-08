from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from vanilla import model_views as views, FormView
from easy_pdf.views import PDFTemplateResponseMixin

from core.mixins import PageTitleMixin, LoginRequiredMixin
from activity.models import Activity
from attendee.models import Attendee
from attendee.forms import AttendeeForm, AttendeePaymentNotificationForm


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
        paginator = self.get_paginator(queryset, self.paginate_by)
        pagination = paginator.page(self.request.GET.get('page', 1))

        context.update(
            search=self.request.GET.get('search'),
            pagination=pagination,
            total_count=queryset.count(),
        )
        return context

    def get_queryset(self):
        queryset = super(AttendeeList, self).get_queryset()
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
        if data is None:
            name = self.request.user.get_full_name()
            email = self.request.user.email
        else:
            name = data.get('name')
            email = data.get('email')

        kwargs.update(initial={
            'name': name,
            'email': email,
        })
        return super(AttendeeJoin, self).get_form(
            data=data, files=files, **kwargs
        )

    def form_valid(self, form):
        self.activity = self.get_activity()
        self.object = form.save(commit=False)
        self.object.profile = self.request.user.profile
        self.object.activity = self.activity

        if not self.activity.price:
            self.object.status = Attendee.CONFIRMED

        try:
            self.object.save()
        except IntegrityError:
            messages.add_message(
                request=self.request, level=messages.ERROR,
                message=_('This user already joined up for this activity!')
            )
            return redirect(self.activity.get_attendee_join_url())
        else:
            message = _('Successfully joined up for this activity!')
            if self.activity.status == self.activity.PRE_SALE:
                message = _(
                    'Successfully joined up for the pre-sale of this activity!'
                )

            messages.add_message(
                request=self.request, level=messages.SUCCESS,
                message=message
            )
            if self.object.activity.price:
                return HttpResponseRedirect(
                    self.object.get_payment_url(full_url=False)
                )
            else:
                return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        self.activity = self.get_activity()
        if self.activity.created_by != self.request.user.profile:
            return self.activity.get_absolute_url()
        return super(AttendeeJoin, self).get_success_url()


class AttendeeDetail(BaseAttendeeView, views.DetailView):
    lookup_field = 'code'
    template_name = 'attendee/detail.html'

    def get_page_title(self):
        return _(u'{attendee}'.format(attendee=self.get_object()))


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


class AttendeePayment(BaseAttendeeView,
                      views.DetailView):
    lookup_field = 'code'
    template_name = 'attendee/payment.html'
    full_page_title = True

    def get_page_title(self):
        activity = self.get_activity()
        return _(u'Payment for {activity}').format(activity=activity)


class AttendeePaymentNotification(BaseAttendeeView, FormView):
    form_class = AttendeePaymentNotificationForm

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AttendeePaymentNotification, self).dispatch(
            *args, **kwargs)

    def get_object(self):
        id_transacao = self.request.POST.get('id_transacao')

        if '-' in id_transacao:
            id_transacao = id_transacao.split('-')[0]

        return self.model.objects.get(code=id_transacao)

    def get_form(self, data, files, **kwargs):
        try:
            kwargs.update(instance=self.get_object())
        except Attendee.DoesNotExist:
            pass

        return super(AttendeePaymentNotification, self).get_form(
            data=data, files=files, **kwargs)

    def return_fail(self, content):
        response = HttpResponse(content=content)
        response.status_code = 400
        return response

    def return_success(self):
        response = HttpResponse()
        response.status_code = 200
        return response

    def form_valid(self, form):
        try:
            self.object = self.get_object()
            self.object.update_payment(form.cleaned_data)
        except(Attendee.DoesNotExist, ValidationError), e:
            return self.return_fail(e.message)
        else:
            return self.return_success()

    def form_invalid(self, form):
        return self.return_fail(form.errors.as_text())


class AttendeeConfirmPayment(BaseAttendeeView, views.UpdateView):
    lookup_field = 'code'

    def post(self, request, *args, **kwargs):
        self.activity = self.get_activity()
        self.object = self.get_object()

        try:
            self.object.update_payment({
                'status_pagamento': Attendee.CONFIRMADO_PELO_ORGANIZADOR,
                'tipo_pagamento': Attendee.NAO_DEFINIDA,
                'moip_code': None,
            })
        except ValidationError, e:
            messages.add_message(
                request=self.request, level=messages.ERROR, message=e.message
            )
        else:
            messages.add_message(
                request=self.request, level=messages.SUCCESS,
                message=_(
                    'Successfully confirmed the attendee "{0}"!'
                ).format(self.object)
            )
        return redirect(self.activity.get_attendee_list_url())
