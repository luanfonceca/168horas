from django.contrib import messages
from django.http import HttpResponseRedirect

from vanilla import TemplateView, UpdateView

from core.models import Profile


class FormValidRedirectMixing(object):
    def success_redirect(self, message):
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())


class PageTitleView(object):
    def get_context_data(self, **kwargs):
        context = super(PageTitleView, self).get_context_data(**kwargs)
        if hasattr(self, 'page_title'):
            context.update(page_title=self.page_title)
        elif hasattr(self, 'get_page_title'):
            context.update(page_title=self.get_page_title())
        return context


class Index(TemplateView):
    template_name = 'index.html'


class Profile(PageTitleView, UpdateView):
    template_name = 'profile.html'
    page_title = 'Profile update'
    model = Profile
    fields = ('state', 'categories',)

    def get_object(self):
        return self.request.user.profile
