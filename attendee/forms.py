from django import forms

from paypal.standard.forms import PayPalPaymentsForm
from localflavor.br.forms import BRCPFField

from attendee.models import Attendee


class AttendeeForm(forms.ModelForm):
    cpf = BRCPFField()

    class Meta:
        model = Attendee
        fields = (
            'name', 'email', 'educational_institution',
            'cpf', 'phone'

        )


class AttendeePaymentForm(PayPalPaymentsForm):
    pass
