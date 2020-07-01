from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Count
from django.db.models.functions import TruncDate,TruncMonth
from django.utils.timezone import utc

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from django.http import HttpResponse

# from matplotlib import pyplot as plt

from rest_framework.views import APIView
from rest_framework.response import Response
from mentee_panel.accounts.models import *
User = get_user_model()

def get_data(request, *args, **kwargs):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data) # http response


class ChartData2(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # plt.plot([1,2,3],[5,7,4])
        # plt.show()
        mentee_count = RegisteredUser.objects.filter(user_type='1').count()
        mentor_count = RegisteredUser.objects.filter(user_type='2').count()
        labels = ["Mentee", "Mentor"]
        default_items = [mentee_count, mentor_count]
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)

class ChartData3(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        result = RegisteredUser.objects.extra(select={'day': 'date( created_on )'}).values('day').annotate(available=Count('created_on'))
        labels=[]
        default_items=[]
        for r in result:
            labels.append(str(r['day']))
            default_items.append(r['available'])

        print(default_items)
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)

class ChartData4(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # plt.plot([1,2,3],[5,7,4])
        # plt.show()
        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)

        fig, ax = plt.subplots()
        ax.plot(t, s)
        ax.set(xlabel='time (s)', ylabel='voltage (mV)',
           title='About as simple as it gets, folks')
        ax.grid()

        response = HttpResponse(content_type = 'image/png')
        canvas = FigureCanvasAgg(fig)
        canvas.print_png(response)
        return response

        # labels = ["Mentee", "Mentor"]
        # default_items = [mentee_count, mentor_count]
        # data = {
        #         "labels": labels,
        #         "default": default_items,
        # }
        # return Response(data)
