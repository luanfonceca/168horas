# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.core.paginator import InvalidPage
from django.contrib import messages
from django.http import HttpResponseRedirect

from vanilla import model_views as views

from core.mixins import (
    PageTitleMixin, BreadcrumbMixin, OrganizerRequiredMixin,
    FormValidRedirectMixing, LoginRequiredMixin
)
from activity.models import Activity
from proposal.models import Proposal, Author
from proposal.forms import (
    ProposalForm, CustomSIPAXProposalForm
)


class BaseProposalView(PageTitleMixin, BreadcrumbMixin):
    model = Proposal
    form_class = ProposalForm
    lookup_field = 'activity_slug'

    def get_context_data(self, **kwargs):
        context = super(BaseProposalView, self).get_context_data(**kwargs)
        context.update(activity=self.get_activity())
        return context

    def get_activity(self):
        return get_object_or_404(
            Activity,
            slug=self.kwargs.get('activity_slug'))

    def get_page_title(self):
        self.activity = self.get_activity()

        return self.page_title or self.activity.title


class ProposalList(BaseProposalView,
                   views.ListView):
    template_name = 'proposal/list.html'
    paginate_by = 30
    allow_empty = True
    full_page_title = True

    def get_breadcrumbs(self):
        self.activity = self.get_activity()

        return [{
            'url': self.activity.get_absolute_url(),
            'title': self.activity.title
        }, {
            'url': self.activity.get_proposal_list_url(),
            'title': _(u'Proposals')
        }]

    def get_context_data(self, **kwargs):
        context = super(ProposalList, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        paginator = self.get_paginator(queryset, self.paginate_by)
        pagination = paginator.page(self.request.GET.get('page', 1))

        context.update(
            search=self.request.GET.get('search'),
            pagination=pagination,
            total_count=queryset.count(),
        )
        return context

    def paginate_queryset(self, queryset, page_size):
        """
        Paginates a queryset, and returns a page object.
        """
        paginator = self.get_paginator(queryset, page_size)
        page_kwarg = self.kwargs.get(self.page_kwarg)
        page_query_param = self.request.GET.get(self.page_kwarg)
        page_number = page_kwarg or page_query_param or 1
        try:
            page_number = int(page_number)
        except ValueError:
            if page_number == 'last':
                page_number = paginator.num_pages
            else:
                msg = "Page is not 'last', nor can it be converted to an int."
                raise InvalidPage(_(msg))

        try:
            return paginator.page(page_number)
        except InvalidPage as exc:
            msg = 'Invalid page (%s): %s'
            raise InvalidPage(_(msg % (page_number, str(exc))))

    def get(self, request, *args, **kwargs):
        try:
            return super(ProposalList, self).get(request, *args, **kwargs)
        except InvalidPage:
            messages.add_message(
                request=self.request, level=messages.WARNING,
                message=_('This page is empty, you are redirect to the first!')
            )
            request.GET = request.GET.copy()
            request.GET['page'] = '1'
            return super(ProposalList, self).get(request.GET, *args, **kwargs)

    def get_queryset(self):
        queryset = super(ProposalList, self).get_queryset()
        self.activity = self.get_activity()
        user = self.request.user
        queryset = queryset.filter(activity=self.activity)

        if not user.is_staff and user.profile != self.activity.created_by:
            queryset = queryset.filter(created_by=user.profile)

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset


class ProposalCreate(BaseProposalView,
                     LoginRequiredMixin,
                     views.CreateView):
    template_name = 'proposal/form.html'
    full_page_title = True

    def get_breadcrumbs(self):
        self.activity = self.get_activity()

        return [{
            'url': self.activity.get_absolute_url(),
            'title': self.activity.title
        }, {
            'url': self.activity.get_proposal_list_url(),
            'title': _(u'Proposals')
        }, {
            'url': self.activity.get_proposal_create_url(),
            'title': _('Create')
        }]

    def get_form_class(self):
        self.activity = self.get_activity()

        if self.activity.slug == 'sipex-minicursos':
            return CustomSIPAXProposalForm
        return ProposalForm

    def form_valid(self, form):
        data = form.cleaned_data
        self.activity = self.get_activity()
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user.profile
        self.object.activity = self.activity
        self.object.save()

        if data.get('author1_name') and data.get('author1_email'):
            Author.objects.create(
                name=data.get('author1_name'),
                email=data.get('author1_email'),
                proposal=self.object
            )
        if data.get('author2_name') and data.get('author2_email'):
            Author.objects.create(
                name=data.get('author2_name'),
                email=data.get('author2_email'),
                proposal=self.object
            )
        if data.get('author3_name') and data.get('author3_email'):
            Author.objects.create(
                name=data.get('author3_name'),
                email=data.get('author3_email'),
                proposal=self.object
            )
        if data.get('author4_name') and data.get('author4_email'):
            Author.objects.create(
                name=data.get('author4_name'),
                email=data.get('author4_email'),
                proposal=self.object
            )
        if data.get('author5_name') and data.get('author5_email'):
            Author.objects.create(
                name=data.get('author5_name'),
                email=data.get('author5_email'),
                proposal=self.object
            )


        message = _(
            'Successfully joined up for the pre-sale of this activity!'
        )
        messages.add_message(
            request=self.request, level=messages.SUCCESS,
            message=message
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        self.activity = self.get_activity()
        return self.activity.get_proposal_list_url()


class ProposalUpdate(BaseProposalView,
                     FormValidRedirectMixing,
                     views.UpdateView):
    template_name = 'attendee/form.html'
    full_page_title = True
    page_title = _('Update')
    lookup_field = 'slug'
    success_message = _('Proposal updated.')

    def get_breadcrumbs(self):
        self.activity = self.get_activity()
        self.object = self.get_object()

        return [{
            'url': self.activity.get_absolute_url(),
            'title': self.activity.title
        }, {
            'url': self.activity.get_proposal_list_url(),
            'title': _(u'Proposals')
        }, {
            'url': self.object.get_update_url(),
            'title': _('Update')
        }]

    def get_success_url(self):
        self.activity = self.get_activity()
        return self.activity.get_proposal_list_url()


class ProposalDetail(BaseProposalView,
                     views.DetailView):
    lookup_field = 'slug'
    template_name = 'proposal/detail.html'

    def get_page_title(self):
        return _(u'{proposal}'.format(proposal=self.get_object()))

    def get_breadcrumbs(self):
        self.activity = self.get_activity()
        self.object = self.get_object()
        user = self.request.user
        is_organizer = user.profile == self.activity.created_by

        breadcrumbs = [{
            'url': self.activity.get_absolute_url(),
            'title': self.activity.title
        }, {
            'url': self.activity.get_proposal_list_url(),
            'title': _('Proposals')
        }, {
            'url': self.object.get_absolute_url(),
            'title': self.object.name
        }]

        if not any([user.is_staff, is_organizer]):
            breadcrumbs.pop(1)

        return breadcrumbs
