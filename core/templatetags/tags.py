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
