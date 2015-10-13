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
