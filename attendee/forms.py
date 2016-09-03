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
    holder_name = forms.CharField(label='Nome impresso no cartao')
    holder_cpf = BRCPFField(label='CPF do proprietario do cartao')
    birth_date = forms.DateField()
    card_hash = forms.CharField(widget=forms.HiddenInput())
    public_key = forms.CharField(widget=forms.HiddenInput(), initial=(
        '-----BEGIN PUBLIC KEY-----'
        'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsXkulsKdAQLMH/zjzTLf'
        '0lrbgulfb6ZShEtRpmDnyX93EQqPdez7LyptvQBeTC+0pN57rNcWen9ApdsIMsNr'
        'YHjNQf/kI4Ka7Xnlx0U/v7bW1D8teDoD5glBTXLjU8hRi7qlOpupiPx4ldSnK9Jj'
        'tYApWuZMiCpWh/YRAlNW/N+ffm7ulq6H2atmgd+OFB2SghpbRJkqJiLaNJW8UkaR'
        'oXLHkF5WJD/RPrCxsZztYJQThxLX5gBgZ12YG5+7G26Ad/mWkPqF0GLSkd1gcnbP'
        'vF9Nw3ckKaIvh4Q4Vp3XI1hLvX41lg9CBxPPHkiJwM1M1coF9xsMP7kpJ2eujMBd'
        'mwIDAQAB'
        '-----END PUBLIC KEY-----'
    ))
    installments = forms.ChoiceField(label='Parcelas')

    class Meta:
        model = Attendee
        fields = (
            'credit_card', 'year', 'month', 'cvv',
            'holder_name', 'holder_cpf',
            'birth_date', 'public_key', 'card_hash'
        )

    def __init__(self, *args, **kwargs):
        super(AttendeePaymentForm, self).__init__(*args, **kwargs)
        choices = self.instance.activity.get_installment_choices()
        self.fields['installments'].choices = choices
