from django import forms
from django.utils.translation import ugettext as _


class CustomSignupForm(forms.Form):
    full_name = forms.CharField(
        required=True, label=_('Full Name'),
        widget=forms.TextInput(attrs={'placeholder': _('Full Name')}))

    def signup(self, request, user):
        full_name = self.cleaned_data.get('full_name').title().split(' ')

        try:
            user.first_name = full_name[0]
            user.last_name = ' '.join(full_name[1:])
        except:
            user.first_name = self.cleaned_data.get('full_name')
        finally:
            user.save()


class ContactForm(forms.Form):
    name = forms.CharField(
        required=True, label=_('Name'),
        widget=forms.TextInput(attrs={'placeholder': _('Name')}))
    email = forms.CharField(
        required=True, label=_('Email'),
        widget=forms.EmailInput(attrs={'placeholder': _('Email')}))
    message = forms.CharField(
        required=True, label=_('Message'),
        widget=forms.Textarea(attrs={'placeholder': _('Message')}))
