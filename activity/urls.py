from django.conf.urls import patterns, url

from activity import views

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=views.ActivityList.as_view(),
        name='list'),
    url(regex=r'^create/$',
        view=views.ActivityCreate.as_view(),
        name='create'),
    url(regex=r'^(?P<slug>[\w-]+)/$',
        view=views.ActivityDetail.as_view(),
        name='detail'),
    url(regex=r'^(?P<slug>[\w-]+)/update/$',
        view=views.ActivityUpdate.as_view(),
        name='update'),
    url(regex=r'^(?P<slug>[\w-]+)/delete/$',
        view=views.ActivityDelete.as_view(),
        name='delete'),
)
