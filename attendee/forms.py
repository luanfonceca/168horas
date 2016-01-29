from django import forms

from attendee.models import Attendee


class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ('name', 'email', 'cpf', 'phone')
