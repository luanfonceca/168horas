from django.contrib.auth.models import User
from django.test import override_settings

from model_mommy import mommy
from django_webtest import WebTest

from category.models import Category
from activity.models import Activity
from attendee.models import Attendee


class AttendeeTest(WebTest):
    fixtures = ['user.json']

    def setUp(self):
        self.user = User.objects.get(username='user')
        self.category = mommy.make(Category, title='Praesent nec nisl')
        self.activity = mommy.make(
            Activity, title='Nunc nulla',
            categories=[self.category], price=99.99)

    @override_settings(LANGUAGE_CODE='pt-BR')
    def test_credit_card_view(self):
        join_page = self.app.get(
            self.activity.get_attendee_join_url(),
            user=self.user
        )
        join_page.form['cpf'] = '08287928443'
        join_page.form['phone'] = '+558487124408'
        payment_page = join_page.form.submit().follow()

        attendee = payment_page.context['object']
        self.assertIsNot(attendee.moip_order_id, None)

        payment_page.form['credit_card'] = '5105105105105100'
        payment_page.form['cvv'] = '123'
        payment_page.form['holder_name'] = attendee.name
        payment_page.form['holder_cpf'] = attendee.cpf
        payment_page.form['month'] = '12'
        payment_page.form['year'] = '2020'
        payment_page.form['birth_date'] = '24/05/1992'
        payment_page.form['installments'] = '4'

        payment_page.form.submit()

        attendee = Attendee.objects.get(pk=attendee.pk)
        self.assertIsNot(attendee.moip_payment_id, None)
        self.assertIsNot(attendee.moip_payment_status, None)

    @override_settings(LANGUAGE_CODE='pt-BR')
    def test_boleto_view(self):
        join_page = self.app.get(
            self.activity.get_attendee_join_url(),
            user=self.user
        )
        join_page.form['cpf'] = '08287928443'
        join_page.form['phone'] = '+558487124408'
        payment_page = join_page.form.submit().follow()

        attendee = payment_page.context['object']
        self.assertIsNot(attendee.moip_order_id, None)

        self.app.get(
            attendee.get_payment_boleto_url(),
            user=self.user
        )

        attendee = Attendee.objects.get(pk=attendee.pk)
        boleto_page = self.app.get(
            attendee.get_payment_boleto_url(),
            user=self.user
        )
        expected_url = (
            'https://checkout-sandbox.moip.com.br/boleto/{}/print/'
        ).format(attendee.moip_payment_id)

        self.assertIsNot(attendee.moip_payment_id, None)
        self.assertIsNot(attendee.moip_payment_status, None)
        self.assertEquals(boleto_page.url, expected_url)

    @override_settings(LANGUAGE_CODE='pt-BR')
    def test_boleto_reopen_view(self):
        join_page = self.app.get(
            self.activity.get_attendee_join_url(),
            user=self.user
        )
        join_page.form['cpf'] = '08287928443'
        join_page.form['phone'] = '+558487124408'
        payment_page = join_page.form.submit().follow()

        attendee = payment_page.context['object']
        self.assertIsNot(attendee.moip_order_id, None)

        self.app.get(
            attendee.get_payment_boleto_url(),
            user=self.user
        )

        attendee = Attendee.objects.get(pk=attendee.pk)
        boleto_page = self.app.get(
            attendee.get_payment_boleto_url(),
            user=self.user
        )
        expected_url = (
            'https://checkout-sandbox.moip.com.br/boleto/{}/print/'
        ).format(attendee.moip_payment_id)

        self.assertIsNot(attendee.moip_payment_id, None)
        self.assertIsNot(attendee.moip_payment_status, None)
        self.assertEquals(boleto_page.url, expected_url)

        # Reopen it
        boleto_page = self.app.get(
            attendee.get_payment_boleto_url(),
            user=self.user
        )
        expected_url = (
            'https://checkout-sandbox.moip.com.br/boleto/{}/print/'
        ).format(attendee.moip_payment_id)

        self.assertEquals(boleto_page.url, expected_url)
