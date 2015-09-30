from django.conf.urls import patterns, include, url

from course.views import CourseList

urlpatterns = patterns(
    '',

    # Apps
    url(r'^', include('core.urls')),
    url(r'^$', CourseList.as_view(), name='index'),
    url(r'^courses/', include('course.urls', namespace='course')),
)
