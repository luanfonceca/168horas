from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.translation import ugettext as _
from django.utils.timezone import datetime
from django.template.loader import render_to_string
from django.core.mail import send_mail

from PIL import Image
import requests

from django_extensions.db.fields import CreationDateTimeField, SlugField
from django_extensions.db.models import TitleSlugDescriptionModel

from web168h import settings


class ActivityManager(models.QuerySet):
    def is_public(self):
        return self.filter(
            ~Q(status=Activity.DRAFT) & ~Q(status=Activity.PRIVATE)
        )

    def get_next(self):
        return self.filter(
            models.Q(scheduled_date__isnull=True) |
            models.Q(scheduled_date__gte=datetime.today())
        ).extra(
            select=dict(date_is_null='scheduled_date IS NULL'),
            order_by=['date_is_null', 'scheduled_date'],
        )


class Activity(TitleSlugDescriptionModel):
    DRAFT, PRIVATE, PRE_SALE, PUBLISHED, SOLDOUT, CLOSED = range(6)
    STATUS_CHOICES = (
        (DRAFT, _('Draft')), (PRIVATE, _('Private')),
        (PRE_SALE, _('Pre-sale')), (PUBLISHED, _('Published')),
        (SOLDOUT, _('Soldout')), (CLOSED, _('Closed')),
    )

    link = models.URLField(_(u'Link'), max_length=300, null=True, blank=True)
    scheduled_date = models.DateField(_(u'Date'), null=True, blank=True)
    hours = models.IntegerField(
        null=True, blank=True,
        help_text=_('Total of hours to be used in the Certificate.'))
    created_at = CreationDateTimeField(_(u'Created At'))
    is_published = models.BooleanField(_(u'Is Published'), default=True)
    is_public = models.BooleanField(_(u'Is Public'), default=True)
    is_organizer = models.BooleanField(_(u'Is Organizer'), default=False)
    is_online = models.BooleanField(default=False)
    photo = models.ImageField(
        _(u'Event photo'),
        upload_to='photos/', null=True, blank=True,
        help_text=_('Images in the resolution: 400x400.'))
    location = models.CharField(
        _(u'Location'), max_length=500, null=True, blank=True)
    place_id = models.CharField(
        _(u'Place id'), max_length=50, null=True, blank=True)
    capacity = models.IntegerField(
        _(u'Capacity'), default=50, null=True, blank=True)
    price = models.DecimalField(
        _(u'Price'), max_digits=10, decimal_places=2, null=True, blank=True)
    short_url = SlugField(
        _('Short url'), max_length=50,
        null=True, blank=True,
        help_text=_('Result will be like: http://168h.com.br/my-activity/'))
    status = models.SmallIntegerField(
        _('Status'), choices=STATUS_CHOICES, default=PUBLISHED)
    embedded_schedule = models.TextField(
        _(u'Embedded Schedule'), max_length=2000, null=True, blank=True)

    # relations
    created_by = models.ForeignKey(
        verbose_name=_(u'Created by'),
        to='core.Profile',
        null=True, blank=True,
        related_name='activities')
    categories = models.ManyToManyField(
        verbose_name=_(u'Categories'),
        to='category.Category',
        related_name='activities')
    attendees = models.ManyToManyField(
        verbose_name=_(u'Attendees'),
        to='core.Profile',
        through='attendee.Attendee',
        related_name='activities+')
    organizers = models.ManyToManyField(
        verbose_name=_(u'Categories'),
        to='core.Profile',
        related_name='managed_activities')

    # managers
    objects = ActivityManager.as_manager()

    class Meta:
        verbose_name = _(u'Activity')
        verbose_name_plural = _(u'Activities')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('activity:detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('activity:update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('activity:delete', kwargs={'slug': self.slug})

    def get_attendee_join_url(self):
        return reverse('attendee:join', kwargs={'activity_slug': self.slug})

    def get_attendee_shuffle_url(self):
        return reverse('attendee:shuffle', kwargs={'activity_slug': self.slug})

    def get_attendee_payment_url(self, profile):
        attendee = self.attendee_set.get(profile=profile)
        return reverse('attendee:payment', kwargs={
            'activity_slug': self.slug,
            'code': attendee.code
        })

    def get_attendee_list_url(self):
        return reverse('attendee:list', kwargs={'activity_slug': self.slug})

    @property
    def get_photo_url(self):
        return '{0}/{1}'.format(settings.MEDIA_URL, self.photo)

    @property
    def get_full_absolute_url(self):
        return 'http://{domain}{url}'.format(
            domain=Site.objects.get_current().domain,
            url=reverse('activity:detail', kwargs={
                'slug': self.slug,
            })
        )

    @property
    def get_full_short_url(self):
        return 'http://{domain}{url}'.format(
            domain=Site.objects.get_current().domain,
            url=reverse('activity_short_url', kwargs={
                'short_url': self.short_url,
            })
        )

    def get_installment_choices(self):
        def get_installment_price(installment, price):
            return '{} x R$ {:.2f}'.format(
                installment, price / installment
            ).replace('.', ',')

        return [
            (installment, get_installment_price(installment, self.price))
            for installment in range(1, 13)
        ]

    @property
    def is_closed(self):
        if self.slug == 'flisol-natal-2016':
            return True
        return False

    def get_attended_ones(self):
        return self.attendee_set.filter(attended_at__isnull=False)

    def check_all(self):
        return self.attendee_set.update(attended_at=datetime.now())

    def send_certificates(self):
        attendees = self.get_attended_ones().values('name', 'code', 'email')
        subject = _(u'Certificate from "{}"!').format(self.title)

        def get_full_certificate_url(slug, code):
            return 'http://{domain}{url}'.format(
                domain=Site.objects.get_current().domain,
                url=reverse('attendee:certificate', kwargs={
                    'activity_slug': slug,
                    'code': code
                })
            )

        for attendee in attendees:
            context = {
                'object': self,
                'name': attendee.get('name'),
                'certificate_url': get_full_certificate_url(
                    self.slug, attendee.get('code'))
            }
            message = render_to_string(
                'mailing/certificate_attendee.txt', context)
            html_message = render_to_string(
                'mailing/certificate_attendee.html', context)
            recipients = [settings.EMAIL_168HORAS, attendee.get('email')]

            send_mail(
                subject=subject, message=message, html_message=html_message,
                from_email=settings.NO_REPLY_EMAIL, recipient_list=recipients
            )

    def get_location(self):
        if not self.location:
            return None

        response = requests.get(
            'http://maps.google.com/maps/api/geocode/json?',
            params=dict(address=self.location, sensor=True)
        )
        if response.ok:
            data = response.json()
            try:
                result = data.get('results')[0]
            except IndexError:
                return None
            else:
                return result.get('geometry').get('location').values()

    @property
    def get_price_as_cents(self):
        return int(self.price * 100)

    @property
    def formatted_price(self):
        price = self.price

        if not price:
            return _('Free')

        if self.price % 1 == 0:
            price = self.price // 1

        return 'R${}'.format(price)

    def notify_pre_sale_organizer(self, attendee):
        context = {
            'object': self,
            'attendee': attendee,
        }
        message = render_to_string(
            'mailing/pre_sale_notification.txt', context)
        html_message = render_to_string(
            'mailing/pre_sale_notification.html', context)
        subject = _(u'{0} joined on pre-sale to "{1}"!').format(
            attendee.name, self.title)
        recipients = [
            settings.EMAIL_168HORAS,
            self.created_by.organizer_email
        ]

        send_mail(
            subject=subject, message=message, html_message=html_message,
            from_email=settings.NO_REPLY_EMAIL, recipient_list=recipients
        )

    def notify_payment_organizer(self, attendee):
        context = {
            'object': self,
            'attendee': attendee,
        }
        message = render_to_string(
            'mailing/payment_notification.txt', context)
        html_message = render_to_string(
            'mailing/payment_notification.html', context)
        subject = _(u'{0} pay the subscription to "{1}"!').format(
            attendee.name, self.title)
        recipients = [settings.EMAIL_168HORAS, self.created_by.organizer_email]

        send_mail(
            subject=subject, message=message, html_message=html_message,
            from_email=settings.NO_REPLY_EMAIL, recipient_list=recipients
        )


def resize_activity_photo(sender, instance, **kwargs):
    try:
        image = Image.open(instance.photo.path)
    except ValueError:
        return

    if (image.width, image.height) == (400, 400):
        return

    image = image.resize((400, 400), Image.ANTIALIAS)
    image.save(instance.photo.path, quality=90)


post_save.connect(resize_activity_photo, sender=Activity)
