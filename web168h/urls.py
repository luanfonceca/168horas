from django.conf.urls import patterns, include, url, static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from web168h import settings


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
    url(r'^categories/', include('category.urls', namespace='category')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'}),
) + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
