from django.conf import settings


def google_analytics(request):
    """
    Use the variables returned in this function to
    render your Google Analytics tracking code template.
    """
    property_id = getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_ID', False)
    analytics_domain = getattr(settings, 'GOOGLE_ANALYTICS_DOMAIN', False)
    if not settings.DEBUG and property_id and analytics_domain:
        return {
            'GOOGLE_ANALYTICS_PROPERTY_ID': property_id,
            'GOOGLE_ANALYTICS_DOMAIN': analytics_domain,
        }
    return {}
