from django.conf.urls import patterns, include, url, static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from web168h import settings
from core import views
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
    url(r'^categories/', include('category.urls', namespace='category')),
    url(r'^a/(?P<short_url>[\w-]+)/',
        view=ActivityDetailShortUrl.as_view(),
        name='activity_short_url'),
    url(r'^payments/notification/',
        view=AttendeePaymentNotification.as_view(),
        name='attendee_payments_notification'),

    # Authentication urls
    url(r'^accounts/signup/',
        view=views.CustomSignupView.as_view(),
        name='account_signup'),
    url(r'^accounts/login/',
        view=views.CustomLoginView.as_view(),
        name='account_login'),
    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'}),
    url(regex=r'^accounts/profile/$',
        view=views.ProfileView.as_view(),
        name='account_profile'),
    url(r'^accounts/password/change',
        view=views.CustomPasswordChangeView.as_view(),
        name='account_change_password'),
    url(r'^accounts/password/set',
        view=views.CustomPasswordSetView.as_view(),
        name='account_set_password'),
    url(r'^accounts/password/reset/$',
        view=views.CustomPasswordResetView.as_view(),
        name='account_reset_password'),
    url(r'^accounts/password/reset/done/$',
        view=views.CustomPasswordResetDoneView.as_view(),
        name='account_reset_password_done'),
    url(r'^accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$',
        view=views.CustomPasswordResetFromKeyView.as_view(),
        name='account_reset_password_from_key'),
    url(r'^accounts/password/reset/key/done/$',
        view=views.CustomPasswordResetFromKeyDoneView.as_view(),
        name='account_reset_password_from_key_done'),
    url(r'^accounts/', include('allauth.urls')),
) + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
