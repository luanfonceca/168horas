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
    url(regex=r'^send_certificates/$',
        view=views.AttendeeJoin.as_view(),
        name='send_certificates'),
    url(regex=r'^export/$',
        view=views.ExportAttendeeList.as_view(),
        name='export'),
)
