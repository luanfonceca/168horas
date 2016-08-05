from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.core.mail import send_mail

from vanilla import TemplateView, UpdateView, FormView
from allauth.account import views as account_views

from core import mixins
from core.models import Profile
from core.forms import ContactForm
from web168h import settings


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


class ContactView(mixins.PageTitleMixin,
                  mixins.FormValidRedirectMixing,
                  FormView):
    template_name = 'contact.html'
    page_title = _('Get in touch')
    full_page_title = True
    success_url = reverse_lazy('contact')
    success_message = _('Thanks, we will contact you soon!')
    form_class = ContactForm

    def form_valid(self, form):
        data = form.cleaned_data

        send_mail(
            subject='Contato pelo Site',
            message=data.get('message'), html_message=data.get('message'),
            from_email='{name} <{email}>'.format(**data),
            recipient_list=[settings.EMAIL_168HORAS]
        )
        return self.success_redirect(self.get_success_message())


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
