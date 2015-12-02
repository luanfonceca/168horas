from django.contrib import messages
from django.http import HttpResponseRedirect

from vanilla.views import TemplateView


class FormValidRedirectMixing(object):
    def success_redirect(self, message):
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())


class Index(TemplateView):
    template_name = 'index.html'
