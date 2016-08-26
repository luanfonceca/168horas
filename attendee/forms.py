import calendar

from django import forms
from django.utils.timezone import datetime

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


class CustomAttendeeForm(forms.ModelForm):
    cpf = BRCPFField()

    class Meta:
        model = Attendee
        exclude = (
            'code', 'attended_at', 'created_at', 'profile',
            'last_updated_at', 'status', 'moip_status',
            'moip_payment_type', 'moip_code', 'activity'
        )


class AttendeePaymentNotificationForm(forms.Form):
    id_transacao = forms.CharField()
    valor = forms.IntegerField()
    status_pagamento = forms.ChoiceField(choices=Attendee.MOIP_STATUS_CHOICES)
    cod_moip = forms.CharField()
    tipo_pagamento = forms.ChoiceField(
        choices=Attendee.MOIP_PAYMENT_TYPE_CHOICES)
    email_consumidor = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(AttendeePaymentNotificationForm, self).__init__(*args, **kwargs)

    def clean_valor(self):
        price = self.cleaned_data.get('valor')
        if self.instance and \
           self.instance.activity.get_price_as_cents > price:
            raise forms.ValidationError(
                'Activity with a wrong price at this payment.'
            )
        return price

    def clean_email_consumidor(self):
        email = self.cleaned_data.get('email_consumidor')
        if self.instance and self.instance.email != email:
            raise forms.ValidationError(
                'Attendee matching query does not exist.'
            )
        return email

    def clean_status_pagamento(self):
        status = self.cleaned_data.get('status_pagamento')
        return int(status)


class AttendeePaymentForm(forms.ModelForm):
    now = datetime.now()
    EXPIRATION_DATE_YEAR_CHOICES = [
        (year, str(year)[2:])
        for year in xrange(now.year, now.year + 11)
    ]

    EXPIRATION_DATE_MONTH_CHOICES = [
        (month, '%02d' % month)
        for month in xrange(1, 13)
    ]

    credit_card = forms.CharField(required=True)
    month = forms.ChoiceField(
        label='MM',
        choices=EXPIRATION_DATE_MONTH_CHOICES)
    year = forms.ChoiceField(
        label='YYYY',
        choices=EXPIRATION_DATE_YEAR_CHOICES)
    cvv = forms.CharField(label='CVV')
    name = forms.CharField(label='Nome impresso no cartao')
    birth_date = forms.DateField()
    cpf = BRCPFField()
    phone = forms.CharField()

    class Meta:
        model = Attendee
        fields = (
            'credit_card', 'year', 'month', 'cvv',
            'name', 'birth_date', 'cpf', 'phone',
        )
