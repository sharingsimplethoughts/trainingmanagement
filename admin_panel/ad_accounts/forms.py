from django import forms
from django.contrib.auth.models import User

from mentee_panel.accounts.models import *


class LoginForm(forms.Form):
    def clean(self):
        em=self.data['email']
        user_qs = User.objects.filter(email=em)
        usertemp = user_qs.exclude(email__isnull=True).exclude(email__iexact='').distinct()
        if usertemp.exists() and usertemp.count()==1:
            userObj=usertemp.first()
        else:
            raise forms.ValidationError('This email id does not exists')
        password=self.data['password']
        checked_pass = userObj.check_password(password)
        if checked_pass:
            if not userObj.is_superuser or not userObj.is_active:
                raise forms.ValidationError('You are not authorised to access this panel')
        else:
            raise forms.ValidationError('Authentication failed')

class ChangePasswordForm(forms.Form):
	oldpassword 	= forms.CharField()
	password 		= forms.CharField()
	confpassword 	= forms.CharField()

	def __init__(self, *args, **kwargs):
		 self.user = kwargs.pop('user',None)
		 super(ChangePasswordForm, self).__init__(*args, **kwargs)
		 self.fields['oldpassword'].strip = False
		 self.fields['password'].strip = False
		 self.fields['confpassword'].strip = False

	def clean(self):
		password = self.cleaned_data.get('password')
		confpassword =self.cleaned_data.get('confpassword')

		if not len(password) >= 8 or not len(confpassword) >= 8:
			raise forms.ValidationError('Password must be at least 8 characters')

		oldpassword = self.cleaned_data.get('oldpassword')
		if not self.user.check_password(oldpassword):
			raise forms.ValidationError('Incorrect old password')

		if password!=confpassword:
			raise forms.ValidationError('Both password fields should be same')

		return self.cleaned_data

class AdminProfileEditForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    phonenumber = forms.CharField(max_length=15)



    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user','None')
        self.ruser=None
        if not self.user:
            self.ruser = RegisteredUser.objects.filter(user=self.user)
        super(AdminProfileEditForm,self).__init__(*args,**kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not self.user.email==email:
            if email.count('@')>1:
                raise forms.ValidationError('Please provide a valid email')
            try:
                domain=email.split('@')[1]
            except:
                raise forms.ValidationError('Please provide a valid email')
            user_qs=User.objects.filter(email__iexact=email)
            if user_qs.exists():
                raise forms.ValidationError('This email already exists')
            return email
        return email

    def clean_mobile(self):
        mob=self.cleaned_data.get('mobile')
        if not mob==self.ruser.mob:
            if mob.isdigit() and len(mob)<10:
                raise forms.ValidationError('This mobile number is not valid')
            ruser_qs=RegisteredUser.objects.filter(mobile__iexact=mob)
            if ruser_qs.exists():
                raise forms.ValidationError('This mobile number already exists')
            return mob
        return mob
