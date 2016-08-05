from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class OrganizerRequiredMixin(object):
    error_redirect_url = None

    def get_error_redirect_url(self):
        if self.error_redirect_url is None:
            if hasattr(self, 'get_activity'):
                self.activity = self.get_activity()
            else:
                self.activity = self.get_object()

            return self.activity.get_absolute_url()
        return self.error_redirect_url

    def has_permission(self):
        if self.request.user.is_staff:
            return True

        if hasattr(self, 'get_activity'):
            self.activity = self.get_activity()
        else:
            self.activity = self.get_object()

        return self.request.user.profile.is_organizer(self.activity)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.has_permission():
            return super(OrganizerRequiredMixin, self).dispatch(
                *args, **kwargs)

        message = _('You have no permission to access this page.')
        messages.add_message(self.request, messages.ERROR, message)
        return redirect(self.get_error_redirect_url())


class FormValidRedirectMixing(object):
    def success_redirect(self, message, level=messages.SUCCESS):
        messages.add_message(self.request, level, message)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_message(self):
        if self.success_message is not None:
            return self.success_message

    def form_valid(self, form):
        self.object = form.save()
        return self.success_redirect(self.get_success_message())


class PageTitleMixin(object):
    page_title = None
    full_page_title = None

    def get_context_data(self, **kwargs):
        context = super(PageTitleMixin, self).get_context_data(**kwargs)
        context.update(page_title=self.get_page_title())
        context.update(full_page_title=self.get_full_page_title())
        return context

    def get_page_title(self):
        if self.page_title is not None:
            return self.page_title

        if hasattr(self, 'object') and self.object is not None:
            return self.object.title

    def get_full_page_title(self):
        return self.full_page_title


class BreadcrumbMixin(object):
    breadcrumbs = []

    def get_context_data(self, **kwargs):
        context = super(BreadcrumbMixin, self).get_context_data(**kwargs)
        context.update(breadcrumbs=self.get_breadcrumbs())
        return context

    def get_breadcrumbs(self):
        if self.breadcrumbs:
            return self.breadcrumbs
