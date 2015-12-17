from django.conf.urls import patterns, url

from core import views

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=views.Index.as_view(),
        name='index'),
    url(regex=r'^profile/$',
        view=views.Profile.as_view(),
        name='profile'),
)
