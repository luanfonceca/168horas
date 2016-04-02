from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect

from vanilla import TemplateView, UpdateView
from allauth.account import views as account_views

from core import mixins
from core.models import Profile


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update(index_page=True)
        return context

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect('activity:list')
        return super(IndexView, self).get(*args, **kwargs)


class ProfileView(mixins.PageTitleMixin,
                  mixins.LoginRequiredMixin,
                  mixins.FormValidRedirectMixing,
                  UpdateView):
    template_name = 'profile.html'
    model = Profile
    page_title = _('Profile update')
    full_page_title = True
    success_url = reverse_lazy('activity:list')
    success_message = _('Profile updated.')
    fields = (
        'state', 'categories',
        'organizer_name', 'digital_signature', 'cpf', 'cnpj',
        'organizer_email', 'organizer_phone',
    )

    def get_object(self):
        return self.request.user.profile


class CustomLoginView(mixins.PageTitleMixin, account_views.LoginView):
    page_title = _('Sign In')
    full_page_title = True


class CustomSignupView(mixins.PageTitleMixin, account_views.SignupView):
    page_title = _('Sign Up')
    full_page_title = True


class CustomPasswordChangeView(mixins.PageTitleMixin,
                               account_views.PasswordChangeView):
    page_title = _('Change Password')
    full_page_title = True


class CustomPasswordSetView(mixins.PageTitleMixin,
                            account_views.PasswordSetView):
    page_title = _('Set Password')
    full_page_title = True


class CustomPasswordResetView(mixins.PageTitleMixin,
                              account_views.PasswordResetView):
    page_title = _('Password Reset')
    full_page_title = True


class CustomPasswordResetDoneView(mixins.PageTitleMixin,
                                  account_views.PasswordResetDoneView):
    page_title = _('Password Reset')
    full_page_title = True


class CustomPasswordResetFromKeyView(mixins.PageTitleMixin,
                                     account_views.PasswordResetFromKeyView):
    page_title = _('Change Password')
    full_page_title = True


class CustomPasswordResetFromKeyDoneView(
     mixins.PageTitleMixin,
     account_views.PasswordResetFromKeyDoneView):
    page_title = _('Change Password')
    full_page_title = True
