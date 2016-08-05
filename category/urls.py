from django.conf.urls import patterns, url

from category import views

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=views.CategoryList.as_view(),
        name='list'),
    url(regex=r'^create/$',
        view=views.CategoryCreate.as_view(),
        name='create'),
    url(regex=r'^(?P<slug>[\w-]+)/$',
        view=views.CategoryDetail.as_view(),
        name='detail'),
    url(regex=r'^(?P<slug>[\w-]+)/update/$',
        view=views.CategoryUpdate.as_view(),
        name='update'),
    url(regex=r'^(?P<slug>[\w-]+)/delete/$',
        view=views.CategoryDelete.as_view(),
        name='delete'),
    url(regex=r'^(?P<slug>[\w-]+)/export_attendees/$',
        view=views.CategoryAttendeeExport.as_view(),
        name='export_attendees'),
)
