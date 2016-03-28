from django.conf.urls import patterns, url

from core import views

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=views.IndexView.as_view(),
        name='index'),
)
