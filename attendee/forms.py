from django import forms

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
