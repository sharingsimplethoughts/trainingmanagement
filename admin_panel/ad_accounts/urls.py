from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import *

app_name='ad_accounts'

urlpatterns=[
    path('test/',UpdateOnlineStatus.as_view(),name='test'),   ###This needs to remove. As this is for the test of socket of SpoofGame. Even remove the view of this and html mentioned in view which is present is main templates folder
    path('home/',AdminHomeView.as_view(),name='ad_home'),
    path('login/',AdminLoginView.as_view(),name='ad_login'),
    path('logout/',AdminLogoutView.as_view(),name='ad_logout'),

    #password reset by mail
    url(r'^password_reset/$', ResetPasswordView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView, name='password_reset_complete'),

    path('profile/',AdminProfileView.as_view(),name='ad_profile'),
    path('profile/edit/',AdminProfileEditView.as_view(),name='ad_profile_edit'),
    path('change_password/',ChangePasswordView.as_view(),name='a_change_password'),
]
