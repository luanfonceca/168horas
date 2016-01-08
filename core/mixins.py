from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class FormValidRedirectMixing(object):
    def success_redirect(self, message):
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())


class PageTitleMixin(object):
    page_title = None

    def get_context_data(self, **kwargs):
        context = super(PageTitleMixin, self).get_context_data(**kwargs)
        context.update(page_title=self.get_page_title())
        return context

    def get_page_title(self):
        if self.page_title is not None:
            return self.page_title

        if hasattr(self, 'object') and self.object is not None:
            return self.object.title
