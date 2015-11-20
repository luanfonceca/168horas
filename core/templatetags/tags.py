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
    if image is not None:
        return image.name.split('/')[-1]
