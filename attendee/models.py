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


from django_extensions.db.fields import CreationDateTimeField


def code_generate(size=10):
    return ''.join(
        random.choice(
            string.ascii_uppercase + string.digits
        ) for x in range(size))


class Attendee(models.Model):
    name = models.CharField(_('Name'), max_length=300)
    cpf = models.CharField('CPF', max_length=14)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Phone'), max_length=50, blank=True)
    educational_institution = models.CharField(
        _('Educational Institution'), max_length=200, null=True, blank=True)
    code = models.CharField(_('Code'), max_length=10, default=code_generate)
    created_at = CreationDateTimeField(_(u'Created At'))
    attended_at = models.DateTimeField(
        _(u'Attended At'), null=True, blank=True)

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

    def get_payment_url(self, full_url=True):
        url = reverse('attendee:payment', kwargs={
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
        context = {
            'object': self,
            'activity': self.activity,
            'created_by': self.activity.created_by,
        }
        message = render_to_string(
            'mailing/welcome_attendee.txt', context)
        html_message = render_to_string(
            'mailing/welcome_attendee.html', context)
        subject = _(u'Welcome to the "{}"!').format(self.activity.title)
        recipients = [self.profile.user.email]

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

    def send_payment_confirmation(self):
        context = {
            'object': self,
            'activity': self.activity,
            'created_by': self.activity.created_by,
        }
        message = render_to_string(
            'mailing/payment_confirmation.txt', context)
        html_message = render_to_string(
            'mailing/payment_confirmation.html', context)
        subject = _(u'Payment confirmation of the "{}"!').format(self.activity.title)
        recipients = [self.profile.user.email]

        send_mail(
            subject=subject, message=message, html_message=html_message,
            from_email=settings.NO_REPLY_EMAIL, recipient_list=recipients
        )

    def confirm_payment(self):
        if self.payment_status == 'paid':
            raise ValidationError(_('This Attendee was already confirmed.'))
        self.payment_status = 'paid'
        self.save()
        self.send_payment_confirmation()



def send_attendee_joined_email(sender, instance, created, **kwargs):
    if not created:
        return
    instance.send_welcome_email()


post_save.connect(send_attendee_joined_email, sender=Attendee)
