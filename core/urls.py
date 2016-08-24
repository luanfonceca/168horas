from django.conf.urls import patterns, url

from core import views

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=views.IndexView.as_view(),
        name='index'),
    url(regex=r'^features/$',
        view=views.FeaturesView.as_view(),
        name='features'),
    url(regex=r'^contact/$',
        view=views.ContactView.as_view(),
        name='contact'),
)
