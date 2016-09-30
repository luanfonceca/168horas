from django.conf.urls import patterns, include, url, static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from web168h import settings
from activity.views import ActivityDetailShortUrl
from attendee.views import AttendeePaymentNotification

admin.autodiscover()
urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

    # Apps
    url(r'^', include('core.urls')),
    url(r'^events/', include('event.urls', namespace='event')),
    url(r'^activities/', include('activity.urls', namespace='activity')),
    url(r'^activities/(?P<activity_slug>[\w-]+)/attendees/',
        include('attendee.urls', namespace='attendee')),
    url(r'^activities/(?P<activity_slug>[\w-]+)/proposals/',
        include('proposal.urls', namespace='proposal')),
    url(r'^categories/', include('category.urls', namespace='category')),
    url(r'^a/(?P<short_url>[\w-]+)/',
        view=ActivityDetailShortUrl.as_view(),
        name='activity_short_url'),
    url(r'^payments/notification/',
        view=AttendeePaymentNotification.as_view(),
        name='attendee_payments_notification'),

    # External apps
    url(r'^accounts/', include('allauth.urls')),
) + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
