from django.urls import path

from .views import *

app_name='or_ex1'

urlpatterns=[
    path('homescreen/',MentorHomeScreenView.as_view(),name='or_home'),
    path('homescreen/search/',MentorHomeScreenSearchView.as_view(),name='or_home_search'),

    path('settings/list/',OptionListView.as_view(),name='or_option_list'),
    path('settings/list/<int:pk>',OptionDetailView.as_view(),name='or_option_detail'),

    path('subscription_plan/list/',SubscriptionPlanListView.as_view(),name='or_subscription_plan_list'),
    path('subscription_plan/list/<int:pk>',SubscriptionPlanDetailView.as_view(),name='or_subscription_plan_detail'),
    path('subscription_plan/list/<int:pk>/subscribe/',SubscribeView.as_view(),name='or_subscribe'),
]
