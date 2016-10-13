# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django import template
register = template.Library()


@register.filter
def get_error_class(field):
    classes = ['validate']
    if field.errors:
        classes.append('invalid')
    return ' '.join(classes)


@register.filter
def exists_pk(queryset, pk):
    return queryset.filter(pk=pk).exists()


@register.filter
def get_filename(image):
    if image.name is not None:
        return image.name.split('/')[-1]


@register.filter
def already_joined(activity, profile):
    if not activity.price:
        return activity.attendee_set.filter(profile=profile).exists()

    try:
        attendee = activity.attendee_set.get(profile=profile)
    except:
        pass
    else:
        return attendee.status == attendee.CONFIRMED


@register.filter
def already_attended(activity, profile):
    try:
        attendee = activity.attendee_set.get(profile=profile)
    except:
        pass
    else:
        return attendee.attended_at is not None


@register.filter
def get_attendee(activity, profile):
    return activity.attendee_set.get(profile=profile)


@register.filter
def payment_is_pending(activity, profile):
    if not activity.price:
        return False
    try:
        attendee = activity.attendee_set.get(profile=profile)
    except:
        return False
    else:
        return attendee.status != attendee.CONFIRMED


@register.filter
def get_attendee_payment_url(activity, profile):
    return activity.get_attendee_payment_url(profile)


@register.filter
def is_organizer(profile, activity):
    return profile.is_organizer(activity)


@register.filter
def get_organizer_email(attendee):
    activity = attendee.activity
    email = activity.created_by.organizer_email
    if not email:
        email = activity.created_by.user.email
    return email


@register.filter
def get_certificate_subject(attendee):
    return _('I need the certificate from {}').format(attendee.activity)
