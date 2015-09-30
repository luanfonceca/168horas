from django.conf.urls import patterns, include, url
from django.contrib import admin

from course.views import CourseList

admin.autodiscover()
urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

    # Apps
    url(r'^', include('core.urls')),
    url(r'^$', CourseList.as_view(), name='index'),
    url(r'^courses/', include('course.urls', namespace='course')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'})
)
