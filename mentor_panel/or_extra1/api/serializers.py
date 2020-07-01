from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import APIException
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from mentee_panel.accounts.models import *
from mentor_panel.or_accounts.models import *
from mentor_panel.or_extra1.models import *

from mentor_panel.or_accounts.api.serializers import *
from mentor_panel.or_post.api.serializers import *

import logging
logger = logging.getLogger('accounts')

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

detail_url=serializers.HyperlinkedIdentityField(view_name='or_ex1:or_option_detail', lookup_field='pk')
sp_detail_url=serializers.HyperlinkedIdentityField(view_name='or_ex1:or_subscription_plan_detail', lookup_field='pk')
subscribe_url=serializers.HyperlinkedIdentityField(view_name='or_ex1:or_subscribe', lookup_field='pk')

class APIException400(APIException):
    status_code = 400

class OptionListSerializer(serializers.ModelSerializer):
    detail_url=detail_url
    class Meta:
        model=Options
        fields=('id','title','content','detail_url')

class OptionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Options
        fields=('id','title','content','detail_url')

class SubscriptionPlanListSerializer(serializers.ModelSerializer):
    sp_detail_url=sp_detail_url
    class Meta:
        model=SubscriptionPlan
        fields=('plan_name','plan_desc','price','duration_in_months','created_on','sp_detail_url')

class SubscriptionPlanDetailSerializer(serializers.ModelSerializer):
    subscribe_url=subscribe_url
    class Meta:
        model=SubscriptionPlan
        fields=('plan_name','plan_desc','price','duration_in_months','created_on','subscribe_url')
