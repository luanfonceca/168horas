from django.conf.urls import patterns, url

from event import views

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=views.EventList.as_view(),
        name='list'),
    url(regex=r'^create/$',
        view=views.EventCreate.as_view(),
        name='create'),
    url(regex=r'^(?P<slug>[\w-]+)/$',
        view=views.EventDetail.as_view(),
        name='detail'),
    url(regex=r'^(?P<slug>[\w-]+)/update/$',
        view=views.EventUpdate.as_view(),
        name='update'),
    url(regex=r'^(?P<slug>[\w-]+)/delete/$',
        view=views.EventDelete.as_view(),
        name='delete'),
)
