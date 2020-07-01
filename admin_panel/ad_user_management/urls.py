from django.urls import path
from .views import *

app_name='ad_user_management'

urlpatterns=[
    path('mentee/',MenteeListView.as_view(),name='ad_mentee'),
    path('mentor/',MentorListView.as_view(),name='ad_mentor'),
]
