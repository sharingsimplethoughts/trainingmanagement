from django.db import models

from mentee_panel.accounts.models import *
# Create your models here.

class Options(models.Model):
    title=models.CharField(max_length=50,blank=True)
    content=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SubscriptionPlan(models.Model):
    plan_name=models.CharField(max_length=100,)
    plan_desc=models.CharField(max_length=800,)
    price=models.DecimalField(max_digits=10,decimal_places=2,default='0.00',)
    # validity_from=models.DateField(auto_now_add=False,)
    # validity_to=models.DateField(auto_now_add=False,)
    duration_in_months=models.PositiveIntegerField(default=0)
    created_on=models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return self.plan_name

class UserSubscription(models.Model):
    plan=models.ForeignKey(SubscriptionPlan,on_delete=models.CASCADE,related_name='us_plan')
    ruser=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='us_ruser')
    created_on=models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return self.plan.title+'-'+self.ruser.first_name+'-'+self.ruser.last_name
