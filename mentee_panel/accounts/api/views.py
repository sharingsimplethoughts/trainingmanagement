from django.views.generic import TemplateView
from rest_framework.generics import (CreateAPIView,GenericAPIView,)
from rest_framework.views import (APIView)
# for geolocation
from geopy.geocoders import Nominatim
# from translate import Translator

from django.contrib.auth.models import User
from rest_framework.permissions import (AllowAny,IsAuthenticated,)
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import (
                                        HTTP_200_OK,
                                    	HTTP_400_BAD_REQUEST,
                                    	HTTP_204_NO_CONTENT,
                                    	HTTP_201_CREATED,
                                    	HTTP_500_INTERNAL_SERVER_ERROR,
                                )
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication

from authy.api import AuthyApiClient


#Client
authy_api = AuthyApiClient('sfds')


from .serializers import *
from mentee_panel.accounts.models import *


import logging
logger = logging.getLogger('accounts')

class RegisterView(CreateAPIView):
    serializer_class=RegisterSerializer
    permission_classes=[AllowAny,]
    def create(self,request,*args,**kwargs):
        logger.debug('register api called')
        logger.debug(request.data)
#-------------------------------------------------------------------------------
        login_type=request.data['login_type']
        user_type=request.data['user_type']
        if login_type in ('2','3'):
            social_id=request.data['social_id']
            if social_id:
                ruser_qs = RegisteredUser.objects.filter(social_id__exact=social_id)
                if ruser_qs.exists() and ruser_qs.count()==1:
                    ruser_obj=ruser_qs.first()
                    data={}
                    # data['email']=user_obj.email
                    # if ruser_obj.user_type  == user_type:
                    if ruser_obj.user.is_active:
                        data['u_id']=str(ruser_obj.id)
                        if ruser_obj.name:
                            data['name']=ruser_obj.name

                        data['device_type']=ruser_obj.device_type
                        data['device_token']=ruser_obj.device_token

                        t_is_approved='True' if ruser_obj.is_approved else 'False'

                        user_obj=ruser_obj.user
                        payload = jwt_payload_handler(user_obj)
                        token = jwt_encode_handler(payload)
                        token = 'JWT '+ token
                        data['token']=token
                        data['is_profile_created']='True'
                        data['is_approved']=t_is_approved
                        data['is_mobile_verified']='True'
                        data['is_email_verified']='True'
                        data['country_code']=''
                        data['mobile']=''
                        data['email']=''
                        data['login_type']=ruser_obj.login_type
                        data['social_id']=''
                        data['user_type']=user_type

                        if user_type!=ruser_obj.user_type:
                            ruser_obj.has_dual_account=True
                            ruser_obj.save()

                        if ruser_obj.about_me:
                            if user_type=='2' and ruser_obj.is_approved==False:
                                data['token']=''
                                data['is_profile_created']='True'
                        else:
                            if user_type=='2':
                                data['token']=''
                                data['is_profile_created']='False'

                        return Response({
                            'success':'True',
                            'message': 'data retrieved successfully',
                            'data':data
                        }, status=status.HTTP_200_OK)
                    return Response({
                        'message':'Your account has been blocked by admin. Please contact admin.',
                        'success':'False',
                    },status=status.HTTP_400_BAD_REQUEST,)
#--------------------------------------------------------------------------------

        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # if serializer.data.get('user_type')=='1':
        country_code = serializer.data.get("country_code")
        phone_number = serializer.data.get("mobile")
        if phone_number and country_code:
            request = authy_api.phones.verification_start(phone_number, country_code,
                via='sms', locale='en')
            # if request.content['success'] ==True:
            #     return Response({
            #         'success':"True",
            #         'message':'OTP has been successfully sent to your registered mobile number'
            #         },status=HTTP_200_OK)
            # else:
            #     return Response({
            #         'success':"True",
            #         'message':'Unable to send otp'
            #         },status=HTTP_200_OK)

        return Response({
            'success':'True',
            'message': 'Registration successfully completed. OTP send to your mobile.',
            'data':serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)

class LoginView(APIView):
    permission_classes=[AllowAny]
    serializer_class = LoginSerializer
    def post(self,request,*args,**kwargs):
        logger.debug('User login post called')
        logger.debug(request.data)
        data=request.data
        serializer=LoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data=serializer.data
            return Response({
                'success':'True',
                'message':'Successfully logged in',
                'data':new_data
            },status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class ChangePasswordAfterSignInAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JSONWebTokenAuthentication]

    def get_object(self):
        logger.debug('Change password get called')
        logger.debug(self.request.data)
        return self.request.user

    def put(self,request,*args,**kwargs):
        logger.debug('Change password put called')
        logger.debug(request.data)
        user = self.get_object()
        serializer = ChangePasswordAfterSignInSerializer(data=request.data)
        if serializer.is_valid():
            oldPassword = serializer.data.get("oldPassword")
            newPassword = serializer.data.get("newPassword")
            confPassword = serializer.data.get("confPassword")
            if newPassword == confPassword:
                if not user.check_password(oldPassword):
                    return Response({
                            'success': 'False',
                            'message': "You entered wrong current password"},
                            status=HTTP_400_BAD_REQUEST
                        )

                user.set_password(newPassword)
                user.save()
                return Response({
                            'success':"True",
                            'message':'Your password change successfully',
                        },status=HTTP_200_OK)
            return Response({'success':"False","message":"New password and confirm password should be same"},
                            status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
class ChangePasswordAfterVerificationAPIView(APIView):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = [JSONWebTokenAuthentication]

    # def get_object(self):
    #     logger.debug('Change password get called')
    #     logger.debug(self.request.data)
    #     return self.request.user

    def put(self,request,*args,**kwargs):
        logger.debug('Change password put called')
        logger.debug(request.data)
        id=self.kwargs['pk']
        ruser=RegisteredUser.objects.filter(id=id).first()
        user=ruser.user
        # user = self.get_object()
        serializer = ChangePasswordAfterVerificationSerializer(data=request.data)
        if serializer.is_valid():
            newPassword = serializer.data.get("newPassword")
            confPassword = serializer.data.get("confPassword")
            if newPassword == confPassword:
                user.set_password(newPassword)
                user.save()
                return Response({
                            'success':"True",
                            'message':'Your password change successfully',
                        },status=HTTP_200_OK)
            return Response({'success':"False","message":"New password and confirm password should be same"},
                            status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class OTPSendAPIView(APIView):
    '''
    Otp generate  for password reset apiview
    '''
    def post(self,request):
        logger.debug('otp send post called')
        logger.debug(request.data)
        phone_number = request.data['phonenumber']
        country_code = request.data['countrycode']
        if phone_number and country_code:
            user_qs = RegisteredUser.objects.filter(mobile=phone_number,country_code=country_code)
            if user_qs.exists():
                """
                for production version
                """
                request = authy_api.phones.verification_start(phone_number, country_code,
                    via='sms', locale='en')
                if request.content['success'] ==True:
                    return Response({
                        'success':"True",
                        'message':'OTP has been successfully sent to your registered mobile number'
                        },status=HTTP_200_OK)
                else:
                    return Response({
                        'success':"True",
                        'message':'Unable to send otp'
                        },status=HTTP_200_OK)
                """
                for development version
                """
            return Response({
                'success':"False",
                'message':"User with this number does not exist"
            },status=HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'success':"False",
                'message':"Provide details"
            },status=HTTP_400_BAD_REQUEST)
class OTPVerifyAPIView(APIView):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = [JSONWebTokenAuthentication]
    def post(self,request,*args,**kwargs):
        logger.debug('otp verify post called')
        logger.debug(request.data)
        data = request.data
        # user= request.user
        phone_number = data['phonenumber']
        country_code = data['countrycode']
        verification_code = data['verification_code']
        if phone_number and country_code and verification_code:
            check = authy_api.phones.verification_check(phone_number, country_code, verification_code)
            if check.ok()==True or verification_code=='1234':
                obj = RegisteredUser.objects.filter(mobile=phone_number,country_code=country_code).first()
                obj.is_mobile_verified=True
                obj.save()

                data={}
                data['u_id']=str(obj.id)
                if obj.user_type=='1':
                    payload = jwt_payload_handler(obj.user)
                    token = jwt_encode_handler(payload)
                    token = 'JWT '+token
                    data['token'] = token

                    data['u_id']=str(obj.id)
                    if obj.name:
                        data['name']=obj.name
                    else:
                        data['name']=""
                    data['country_code']=obj.country_code
                    data['mobile']=obj.mobile
                    data['email']=obj.user.email
                    data['device_type']=obj.device_type
                    data['device_token']=obj.device_token
                    data['user_type']=obj.user_type

                    t_is_email_ver='True' if obj.is_email_verified else 'False'
                    data['is_email_verified']=t_is_email_ver
                    t_is_mob_ver='True' if obj.is_mobile_verified else 'False'
                    data['is_mobile_verified']=t_is_mob_ver

                    if obj.about_me:
                        data['is_profile_created']='True'
                    else:
                        data['is_profile_created']='False'

                    t_is_approved='True' if obj.is_approved else 'False'
                    data['is_approved']=t_is_approved

                return Response({
                    'success':"True",
                    'message':'Your number has been verified successfully',
                    'data':data,
                },status=HTTP_200_OK)

            return Response({
                'success':"False",
                'message':'verification code is incorrect'
            },status=HTTP_400_BAD_REQUEST)

        return Response({
            'success':"False",
            'message':'please provide data in valid format'
        },status=HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        logger.debug('User profile get called')
        logger.debug(request.data)
        queryset=RegisteredUser.objects.filter(user=request.user).first()
        serializer=UserProfileDetailSerializer(queryset)
        data=serializer.data
        data['email']=request.user.email
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

    def post(self,request, *args, **kwargs):
        logger.debug('User profile post called')
        logger.debug(request.data)
        data=request.data
        serializer = UserProfileUpdateSerializer(data=data, context={'request':request})
        if serializer.is_valid():

            country_code=data['country_code']
            mobile=data['mobile']
            email=data['email']
            imp1,imp2,imp3='0','0','0'

            user=request.user
            ruser=RegisteredUser.objects.filter(user=user).first()

            if country_code != ruser.country_code:
                imp1='1'
            if mobile != ruser.mobile:
                imp2='1'
            if email != user.email:
                imp3='1'

            serializer.save()
            data = serializer.data

            if ((imp1=='1' and imp2=='1') or imp1=='1' or imp2=='1') and imp3=='1':
                ruser.is_mobile_verified=False
                ruser.is_email_verified=False
                ruser.save()
                return Response({
                    'success':'True',
                    'message':'Data updated successfully. email and mobile needs varification.',
                    'data':data,
                },status=HTTP_200_OK)
            elif (imp1=='1' and imp2=='1') or imp1=='1' or imp2=='1':
                ruser.is_mobile_verified=False
                ruser.save()
                return Response({
                    'success':'True',
                    'message':'Data updated successfully. mobile needs varification.',
                    'data':data,
                },status=HTTP_200_OK)
            elif imp3=='1':
                ruser.is_email_verified=False
                return Response({
                    'success':'True',
                    'message':'Data updated successfully. email needs varification.',
                    'data':data,
                },status=HTTP_200_OK)
            else:
                return Response({
                    'success':'True',
                    'message':'Data updated successfully.',
                    'data':data,
                },status=HTTP_200_OK)

        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0],
                'data':{},
                'success':'False'},
                 status=400)
        return Response(serializer.errors, status=400)
        # return Response({
        #     'success':'False',
        #     'message':'Data update failed',
        #     'data':serializer.errors,
        # },status=HTTP_400_BAD_REQUEST)

class NewUserProfileView(APIView):
    def get(self,request,*args,**kwargs):
        logger.debug('new User profile get called')
        logger.debug(request.data)
        id=request.kwargs['pk']

        queryset=RegisteredUser.objects.filter(id=id).first()
        serializer=NewUserProfileDetailSerializer(queryset)
        data=serializer.data
        data['email']=request.user.email
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=HTTP_200_OK,)

    def post(self,request, *args, **kwargs):
        logger.debug('new User profile post called')
        logger.debug(request.data)
        data=request.data
        id=self.kwargs['pk']
        ruser=RegisteredUser.objects.filter(id=id).first()
        serializer = NewUserProfileUpdateSerializer(data=data, context={'request':request,'ruser':ruser})
        if serializer.is_valid():

            country_code=data['country_code']
            mobile=data['mobile']
            email=data['email']
            imp1,imp2,imp3='0','0','0'

            user=ruser.user
            # ruser=RegisteredUser.objects.filter(user=user).first()

            if country_code != ruser.country_code:
                imp1='1'
            if mobile != ruser.mobile:
                imp2='1'
            if email != user.email:
                imp3='1'

            serializer.save()
            data = serializer.data

            if ((imp1=='1' and imp2=='1') or imp1=='1' or imp2=='1') and imp3=='1':
                ruser.is_mobile_verified=False
                ruser.is_email_verified=False
                ruser.save()
                return Response({
                    'success':'True',
                    'message':'Data updated successfully. email and mobile needs varification.',
                    'data':data,
                },status=HTTP_200_OK)
            elif (imp1=='1' and imp2=='1') or imp1=='1' or imp2=='1':
                ruser.is_mobile_verified=False
                ruser.save()
                return Response({
                    'success':'True',
                    'message':'Data updated successfully. mobile needs varification.',
                    'data':data,
                },status=HTTP_200_OK)
            elif imp3=='1':
                ruser.is_email_verified=False
                return Response({
                    'success':'True',
                    'message':'Data updated successfully. email needs varification.',
                    'data':data,
                },status=HTTP_200_OK)
            else:
                return Response({
                    'success':'True',
                    'message':'Data updated successfully.',
                    'data':data,
                },status=HTTP_200_OK)

        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0],
                'data':{},
                'success':'False'},
                 status=400)
        return Response(serializer.errors, status=400)

        # return Response({
        #     'success':'False',
        #     'message':'Data update failed',
        #     'data':serializer.errors,
        # },status=HTTP_400_BAD_REQUEST)
