import random
import string

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import datetime

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import (
    valid_ipn_received, invalid_ipn_received)

from django_extensions.db.fields import CreationDateTimeField


def code_generate(size=10):
    return ''.join(
        random.choice(
            string.ascii_uppercase + string.digits
        ) for x in range(size))


class Attendee(models.Model):
    PENDING, CANCELED, PAID = range(3)
    STATUS_RATES = (
        (PENDING, _('Pending')), (CANCELED, _('Canceled')), (PAID, _('Paid')),
    )

    name = models.CharField(_('Name'), max_length=200)
    cpf = models.CharField('CPF', max_length=14)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Phone'), max_length=50, blank=True)
    code = models.CharField(_('Code'), max_length=10, default=code_generate)
    created_at = CreationDateTimeField(_(u'Created At'))
    attended_at = models.DateTimeField(
        _(u'Attended At'), null=True, blank=True)
    payment_status = models.SmallIntegerField(
        _('Payment Status'), choices=STATUS_RATES, default=PENDING,
        null=True, blank=True)

    # Extra informations
    startup = models.CharField(
        _('Startup'), max_length=50, null=True,
        help_text=_('If you already have one'))
    course = models.CharField(_('Course'), max_length=50, null=True)
    university = models.CharField(_('University'), max_length=50, null=True)
    born_at = models.DateTimeField(_(u'Born At'), null=True)
    expectations = models.TextField(_('Your expectations'), null=True)

    # relations
    activity = models.ForeignKey(
        to='activity.Activity',
        on_delete=models.CASCADE)
    profile = models.ForeignKey(
        to='core.Profile',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = _(u'Attendee')
        verbose_name_plural = _(u'Attendees')
        unique_together = ('activity', 'profile')

    def __unicode__(self):
        return u'{0.name}'.format(self)

    @property
    def has_attended(self):
        return True if self.attended_at else False

    @property
    def get_photo_url(self):
        social = self.profile.user.socialaccount_set.first()
        if social:
            return social.get_avatar_url()
        return static('attendee/img/default-profile.png')

    def get_absolute_url(self):
        return reverse(
            'attendee:list', kwargs={'activity_slug': self.activity.slug}
        ) + '#{.profile.user.username}'.format(self)

    def get_send_email_url(self):
        return 'mailto:{.email}'.format(self)

    def get_certificate_url(self, full_url=True):
        url = reverse('attendee:certificate', kwargs={
            'activity_slug': self.activity.slug,
            'code': self.code,
        })
        if full_url:
            return 'http://{domain}{url}'.format(
                domain=Site.objects.get_current().domain, url=url
            )
        else:
            return url

    def send_welcome_email(self):
        created_by = self.activity.created_by
        context = {
            'name': self.name,
            'activity_title': self.activity.title,
            'organizer_email': created_by.organizer_email,
            'organizer_name': created_by.organizer_name,
            'payment_url': self.activity.get_full_attendee_payment_url(),
            'price': self.activity.price,
            'is_pending': self.payment_status == self.PENDING
        }
        message = render_to_string(
            'mailing/welcome_attendee.txt', context)
        html_message = render_to_string(
            'mailing/welcome_attendee.html', context)
        subject = _(u'Welcome to the "{}"!').format(self.activity.title)
        recipients = [self.email]

        send_mail(
            subject=subject, message=message, html_message=html_message,
            from_email=settings.NO_REPLY_EMAIL, recipient_list=recipients
        )

    def send_payment_confirmation_email(self):
        context = {
            'name': self.name,
            'activity_title': self.activity.title,
            'payment_url': self.activity.get_full_attendee_payment_url(),
        }
        message = render_to_string(
            'mailing/payment_confirmation.txt', context)
        html_message = render_to_string(
            'mailing/payment_confirmation.html', context)
        subject = _(u'Welcome to the "{}"!').format(self.activity.title)
        recipients = [self.email]

        send_mail(
            subject=subject, message=message, html_message=html_message,
            from_email=settings.NO_REPLY_EMAIL, recipient_list=recipients
        )

    def checkin(self):
        if self.attended_at:
            raise ValidationError(_('This Attendee was already checked in.'))
        self.attended_at = datetime.now()
        self.save()

    def uncheck(self):
        if not self.attended_at:
            raise ValidationError(_('This Attendee is not checked in yet.'))
        self.attended_at = None
        self.save()


def send_attendee_joined_email(sender, instance, created, **kwargs):
    if not created:
        return
    instance.send_welcome_email()


def show_me_the_money(sender, **kwargs):
    import ipdb; ipdb.set_trace()
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the business field request. (The user could tamper
        # with those fields on payment form before send it to PayPal)
        if ipn_obj.receiver_email != "receiver_email@example.com":
            # Not a valid payment
            return
        # Undertake some action depending upon `ipn_obj`.
        if ipn_obj.custom == "Upgrade all users!":
            Attendee.objects.update(paid=True)
    # attendee.status = attendee.PAID
    # attendee.save()
    # attendee.send_payment_confirmation_email()


def refuse_to_give_the_money(sender, **kwargs):
    import ipdb; ipdb.set_trace()


valid_ipn_received.connect(show_me_the_money)
invalid_ipn_received.connect(refuse_to_give_the_money)
post_save.connect(send_attendee_joined_email, sender=Attendee)
