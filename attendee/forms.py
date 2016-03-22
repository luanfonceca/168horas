from django import forms

from paypal.standard.forms import PayPalPaymentsForm

from attendee.models import Attendee


class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = (
            'name', 'email', 'cpf', 'phone',
        )


class AttendeeExtraInformationForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = (
            'name', 'email', 'cpf', 'phone',
            'startup', 'course', 'university',
            'born_at', 'expectations',
        )


class AttendeePaymentForm(PayPalPaymentsForm):
    pass
