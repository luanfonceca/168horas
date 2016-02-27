from django.conf.urls import patterns, url

from attendee import views

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=views.AttendeeList.as_view(),
        name='list'),
    url(regex=r'^join/$',
        view=views.AttendeeJoin.as_view(),
        name='join'),
    url(regex=r'^sort/$',
        view=views.AttendeeSort.as_view(),
        name='sort'),
    url(regex=r'^check/(?P<code>[0-9A-Z]+)/$',
        view=views.AttendeeCheck.as_view(),
        name='check'),
    url(regex=r'^uncheck/(?P<code>[0-9A-Z]+)/$',
        view=views.AttendeeUncheck.as_view(),
        name='uncheck'),
    url(regex=r'^certificate/(?P<code>[0-9A-Z]+)/$',
        view=views.AttendeeCertificate.as_view(),
        name='certificate'),
)
