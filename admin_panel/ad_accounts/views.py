from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login ,logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.contrib.auth import views as auth_views
# Create your views here.

from .forms import *
from .password_reset_form import MyPasswordResetForm

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
# from solo.models import *
# Create your views here.


class UpdateOnlineStatus(TemplateView):#LoginRequiredMixin,
    def get(self,request,*args,**kwargs):
        # user = self.request.user
        # ruser=RegisteredUser.objects.filter(user=user).first()
        # msgs=TestModel.objects.filter(ruser=ruser)
        msgs=""
        return render(request, 'page1.html', context={'messages':msgs})


class AdminHomeView(LoginRequiredMixin,TemplateView):
    login_url='ad_accounts:ad_login'
    template_name='index.html'

class AdminLoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        form = LoginForm
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('ad_accounts:ad_home'))
        return render(request, 'ad_accounts/login.php', {'form':form})

    def post(self,request,*args,**kwargs):
        form = LoginForm(data=request.POST or None)
        print(form.errors)
        if form.is_valid():
            em=request.POST['email']
            user_qs= User.objects.get(email=em, is_active=True, is_staff=True, is_superuser=True)
            if not request.POST.getlist('rememberChkBox'):
                request.session.set_expiry(0)
            login(request,user_qs,backend='django.contrib.auth.backends.ModelBackend')
            response = HttpResponseRedirect(reverse('ad_accounts:ad_home'))
            # response.set_cookie['role_admin']
            response.set_cookie(key='id', value=1)
            return response
        return render(request,'ad_accounts/login.php', {'form':form})

class AdminLogoutView(LoginRequiredMixin, TemplateView):
    login_url='ad_accounts:ad_login'
    def get(self, request):
        logout(request)
        response = HttpResponseRedirect(reverse('ad_accounts:ad_home'))
        response.delete_cookie(key='id')
        return response

class ResetPasswordView(auth_views.PasswordResetView):
    form_class = MyPasswordResetForm

class ChangePasswordView(LoginRequiredMixin,TemplateView):
    login_url='ad_accounts:ad_login'
    def get(self,request):
        form = ChangePasswordForm(user=request.user)
        return render(request, 'ad_accounts/changePassword.php',{'form': form})

    def post(self,request):
        user = request.user
        form = ChangePasswordForm(request.POST or None, user=request.user)

        if form.is_valid():
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(reverse('ad_accounts:ad_login'))
        return render(request, 'ad_accounts/changePassword.php',{'form': form})

class AdminProfileView(LoginRequiredMixin, TemplateView):
    login_url='ad_accounts:ad_login'
    def get(self, request, *args, **kwargs):
        form=AdminProfileEditForm
        print(request.user)
        context={}
        context['email']=request.user.email
        ruser=RegisteredUser.objects.filter(user=request.user).first()
        if ruser:
            if ruser.name:
                context['name']=ruser.name
            context['mobile']=ruser.mobile
            context['profile_image']=ruser.profile_image
            # context['background_image']=ruser.background_image
            context['about']=ruser.about_me

        return render(request,'ad_accounts/profile.php',context)

class AdminProfileEditView(LoginRequiredMixin, TemplateView):
    login_url='ad_accounts:ad_login'
    def get(self,request,*args,**kwargs):
        print('inside get')
        form=AdminProfileEditForm
        user=request.user
        context={
            'form':form,
            'email':user.email,
        }
        ruser=RegisteredUser.objects.filter(user=user).first()
        if ruser:
            if ruser.name:
                context['name']=ruser.name

            context['mobile']=ruser.mobile
            context['profile_image']=ruser.profile_image
            # context['background_image']=ruser.background_image
            context['about']=ruser.about_me
        return render(request,'ad_accounts/edit-profile.php',context)

    def post(self,request,*args,**kwargs):
        print('inside post')
        user=request.user
        form=AdminProfileEditForm(data=request.POST or None, user=request.user)
        if form.is_valid():
            print('inside post valid form')
            try:
                ruser=RegisteredUser.objects.filter(user=user).first()
            except:
                ruser=None

            name=request.POST['name']
            email=request.POST['email']
            mobile=request.POST['phonenumber']
            profile_image=request.FILES.get('profileimg')
            # background_image=request.FILES.get('coverimg')
            about=request.POST['about']

            user.email=email
            user.first_name=name.split(' ')[0]
            user.last_name=name.split(' ')[1]
            user.save()

            if ruser:
                ruser.name=name
                ruser.country_code='+971'
                ruser.mobile=mobile
                if profile_image:
                    ruser.profile_image=profile_image
                # if background_image:
                #     ruser.background_image=background_image
                ruser.about_me=about
                ruser.user=user
                ruser.save()
            else:
                country_code='+971'
                RegisteredUser.objects.create(
                    name=name,country_code=country_code,mobile=mobile,
                    profile_image=profile_image,about_me=about,user=user,
                )
            return HttpResponseRedirect(reverse('ad_accounts:ad_profile'))

        print(form.errors)
        return render(request,'ad_accounts/edit-profile.php',{'form':form})
