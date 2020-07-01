from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
import pytz
from django.db.models import Q

from mentee_panel.accounts.models import *
from mentor_panel.or_accounts.models import *

# Create your views here.
class MenteeListView(LoginRequiredMixin,TemplateView):
    login_url='ad_accounts:ad_login'
    def get(self,request,*args,**kwargs):
        afilter=self.request.GET.get('afilter')
        if afilter=='All':
            users = RegisteredUser.objects.filter(user_type=1)
        if afilter=='Online':
            pass
        if afilter=='Offline':
            pass
        return render(request,'ad_user_management/mentee.php',{'users':users,'role':'1'})

class MentorListView(TemplateView):
    def get(self,request,*args,**kwargs):
        users = RegisteredUser.objects.filter(user_type=2)
        return render(request,'ad_user_management/mentor.php',{'users':users,'role':'2'})
