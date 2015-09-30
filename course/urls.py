from django.conf.urls import patterns, url

from course import views

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=views.CourseList.as_view(),
        name='list'),
    url(regex=r'^create/$',
        view=views.CourseCreate.as_view(),
        name='create'),
    url(regex=r'^(?P<slug>[\w-]+)/$',
        view=views.CourseDetail.as_view(),
        name='detail'),
    url(regex=r'^(?P<slug>[\w-]+)/update/$',
        view=views.CourseUpdate.as_view(),
        name='update'),
    url(regex=r'^(?P<slug>[\w-]+)/delete/$',
        view=views.CourseDelete.as_view(),
        name='delete'),
)
