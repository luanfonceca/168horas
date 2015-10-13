from django.conf.urls import patterns, include, url
from django.contrib import admin

from category.views import EventByCategoryList

admin.autodiscover()
urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

    # Apps
    url(r'^', include('core.urls')),
    url(r'^$', EventByCategoryList.as_view(), name='index'),
    url(r'^events/', include('event.urls', namespace='event')),
    url(r'^categories/', include('category.urls', namespace='category')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'})
)
