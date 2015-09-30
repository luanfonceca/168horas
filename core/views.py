from django.contrib import messages
from django.http import HttpResponseRedirect


class FormValidRedirectMixing(object):
    def success_redirect(self, message):
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())
