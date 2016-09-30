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

    # Profile urls
    url(regex=r'^accounts/my_certificates/$',
        view=views.MyCertificates.as_view(),
        name='my_certificates'),
    url(regex=r'^accounts/profile/$',
        view=views.ProfileView.as_view(),
        name='account_profile'),

    # Authentication urls
    url(r'^accounts/signup/',
        view=views.CustomSignupView.as_view(),
        name='account_signup'),
    url(r'^accounts/login/',
        view=views.CustomLoginView.as_view(),
        name='account_login'),
    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'}),
    url(r'^accounts/password/change',
        view=views.CustomPasswordChangeView.as_view(),
        name='account_change_password'),
    url(r'^accounts/password/set',
        view=views.CustomPasswordSetView.as_view(),
        name='account_set_password'),
    url(r'^accounts/password/reset/$',
        view=views.CustomPasswordResetView.as_view(),
        name='account_reset_password'),
    url(r'^accounts/password/reset/done/$',
        view=views.CustomPasswordResetDoneView.as_view(),
        name='account_reset_password_done'),
    url(r'^accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$',
        view=views.CustomPasswordResetFromKeyView.as_view(),
        name='account_reset_password_from_key'),
    url(r'^accounts/password/reset/key/done/$',
        view=views.CustomPasswordResetFromKeyDoneView.as_view(),
        name='account_reset_password_from_key_done'),
)
