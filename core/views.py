from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from vanilla import TemplateView, UpdateView

from core.models import Profile


class FormValidRedirectMixing(object):
    def success_redirect(self, message):
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())


class PageTitleView(object):
    page_title = None

    def get_context_data(self, **kwargs):
        context = super(PageTitleView, self).get_context_data(**kwargs)
        context.update(page_title=self.get_page_title())
        return context

    def get_page_title(self):
        if self.page_title is not None:
            return self.page_title

        if hasattr(self, 'object') and self.object is not None:
            return self.object.title


class LoginRequiredView(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredView, self).dispatch(*args, **kwargs)


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context.update(index_page=True)
        return context


class Profile(PageTitleView, LoginRequiredView, UpdateView):
    template_name = 'profile.html'
    page_title = 'Profile update'
    model = Profile
    fields = ('state', 'categories',)

    def get_object(self):
        return self.request.user.profile
