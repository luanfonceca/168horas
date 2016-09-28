from django.conf.urls import patterns, url

from proposal import views

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=views.ProposalList.as_view(),
        name='list'),
    url(regex=r'^create/$',
        view=views.ProposalCreate.as_view(),
        name='create'),
    url(regex=r'^detail/(?P<slug>[0-9A-Z]+)/$',
        view=views.ProposalDetail.as_view(),
        name='detail'),
    url(regex=r'^update/(?P<slug>[0-9A-Z]+)/$',
        view=views.ProposalUpdate.as_view(),
        name='update'),
)
