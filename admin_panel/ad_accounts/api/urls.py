from django.urls import path

from .views import *

app_name='temp_app'

urlpatterns=[
    # path('api/data/1', get_data, name='api-data'),
    path('api/chart/data/2', ChartData2.as_view(),name='api-data-2'),
    path('api/chart/data/3', ChartData3.as_view(),name='api-data-3'),
    path('api/chart/data/4', ChartData4.as_view(),name='api-data-4'),
]
