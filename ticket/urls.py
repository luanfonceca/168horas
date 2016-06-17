from django.conf.urls import patterns, url

from ticket import views

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=views.TicketList.as_view(),
        name='list'),
    url(regex=r'^create/$',
        view=views.TicketCreate.as_view(),
        name='create'),
    url(regex=r'^(?P<slug>[\w-]+)/$',
        view=views.TicketDetail.as_view(),
        name='detail'),
    url(regex=r'^(?P<slug>[\w-]+)/update/$',
        view=views.TicketUpdate.as_view(),
        name='update'),
    url(regex=r'^(?P<slug>[\w-]+)/delete/$',
        view=views.TicketDelete.as_view(),
        name='delete'),
)
