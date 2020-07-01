from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import APIException
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from mentee_panel.accounts.models import *
from mentor_panel.or_accounts.models import *

import logging
logger = logging.getLogger('accounts')

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class APIException400(APIException):
    status_code = 400

class RegisterSerializer(serializers.ModelSerializer):
#-----------COMMON-------------------
    name = serializers.CharField(allow_blank=True)
    country_code=serializers.CharField(allow_blank=True)
    mobile = serializers.CharField(allow_blank=True)
#----------- ONLY FOR MENTOR------------
    # background = serializers.CharField(allow_blank=True)
    # experience = serializers.CharField(allow_blank=True)
    # category = serializers.CharField(allow_blank=True)
    # declaration = serializers.FileField(required=False,)
    # about_me = serializers.CharField(allow_blank=True)
#------------ ONLY FOR MENTEE------------
    email = serializers.CharField(allow_blank=True, style={'input_type':'email'})
#----------- COMMON ---------------------
    password = serializers.CharField(allow_blank=True,write_only=True,style={'input_type':'password'})

    login_type = serializers.CharField(allow_blank=True)
    social_id = serializers.CharField(allow_blank=True)

    device_type = serializers.CharField(allow_blank=True)

    user_type = serializers.CharField(allow_blank=True)

    message = serializers.CharField(allow_blank=True, read_only=True)
    success = serializers.CharField(allow_blank=True, read_only=True)
    token = serializers.CharField(allow_blank=True,read_only=True)
    u_id = serializers.CharField(allow_blank=True, read_only=True)
    created_on = serializers.CharField(allow_blank=True, read_only=True)
    is_profile_created = serializers.CharField(read_only=True)
    is_approved = serializers.CharField(read_only=True)
    is_mobile_verified = serializers.CharField(read_only=True)
    is_email_verified = serializers.CharField(read_only=True)

    class Meta:
        model=RegisteredUser
        fields=['name', 'country_code', 'mobile',  'email', 'password', 'login_type', 'social_id',
        'device_type', 'device_token', 'user_type', 'message', 'success', 'token',
        'u_id', 'created_on','is_profile_created','is_approved','is_email_verified','is_mobile_verified',]

    def validate(self, data):
        name=data['name']
        country_code=data['country_code']
        mob=data['mobile']

        # background=data['background']
        # experience=data['experience']
        # category=data['category']
        # declaration = self.context['request'].FILES.get('declaration')
        # about_me=data['about_me']
        email=data['email']
        password=data['password']
        login_type=data['login_type']
        social_id=data['social_id']
        device_type=data['device_type']
        device_token=data['device_token']
        user_type=data['user_type']

        if not login_type or login_type=='':
            raise APIException400({
                'success':'False',
                'message':'Please provide login type',
            })
        if login_type not in ('1','2','3'):
            raise APIException400({
                'success':'False',
                'message':'Please provide a valid login type',
            })
        if login_type in ('2','3'):
            if not social_id or social_id=="" :
                raise APIException400({
                    'success':'False',
                    'message':'Please provide social id'
                })
            ruser_qs = RegisteredUser.objects.filter(social_id__exact=social_id)
            if ruser_qs.exists() and ruser_qs.count()==1:
                ruser_obj=ruser_qs.first()

                user_obj=ruser_obj.user
                payload = jwt_payload_handler(user_obj)
                token = jwt_encode_handler(payload)

                # data['country_code']=user_obj.country_code
                # data['mobile']=user_obj.mobile
                data['token']=token
                data['name']=ruser_obj.name
                # data['mobile']=ruser_obj.mobile
                data['device_type']=ruser_obj.device_type
                data['device_token']=ruser_obj.device_token

                raise APIException400({
                    'success':'True',
                    'message':'Social id already exists',
                    'data':data,
                })

        if not name or name=='':
            raise APIException400({
                'success':"False",
                'message':'Name can not be blank',
                })
#************************************************************
        if login_type in ('2','3'):
            print('aaaaa')
            if social_id:
                print('hello')
                if (not country_code or country_code=="") and mob:
                    raise APIException400({
                        'success':"False",
                        'message':'please provide country code',
                        })
                if (not mob or mob=="") and country_code:
                    raise APIException400({
                        'success':"False",
                        'message':'please provide mobile',
                        })
                if mob and country_code:
                    ruo=RegisteredUser.objects.filter(mobile__iexact=mob,country_code__iexact=country_code).first()
                    if ruo:
                        raise APIException400({
                            'success':"False",
                            'message':'User with this mobile is already exists. Please login to continue.',
                            })
                else:
                    country_code='+971'
                    mob=social_id
                if email:
                    print('ccc')
                    user_t=User.objects.filter(email__iexact=email).first()
                    if user_t:
                        raise APIException400({
                            'success':"False",
                            'message':'This email is already registered. Please login to continue.',
                            })
                    else:
                        password='C123M@45'
                else:
                    print('bbbbb')
                    email=social_id+'@xyz63.com'
                    password='C123M@45'
#*************************************************************
        if not country_code or country_code=='':
            raise APIException400({
                'success':'False',
                'message':'country code is required',
            })
        if not mob or mob=='':
            raise APIException400({
                'success':'False',
                'message':'mobile is required',
            })
        if not user_type or user_type=='':
            raise APIException({
                'success':'False',
                'message':'user_type is required',
            })
        if user_type not in ['1','2']:
            raise APIException400({
                'success':'False',
                'message':'Please enter correct format of user_type',
            })

        # if user_type == '1':
            # email validation category
        if not email or email=='':
            raise APIException400({
                'success':'False',
                'message':'email is required',
                })
        allowedDomains = [
        "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
        "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
        "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",
        "email.com", "games.com" , "gmx.net", "hush.com", "hushmail.com", "icloud.com", "inbox.com",
        "lavabit.com", "love.com" , "outlook.com", "pobox.com", "rocketmail.com",
        "safe-mail.net", "wow.com", "ygm.com" , "ymail.com", "zoho.com", "fastmail.fm",
        "yandex.com","iname.com","xyz63.com",
        ]
        if '@' not in email:
            raise APIException400({
                'success':'False',
                'message':'Please provide a valid email',
            })
        else:
            domain = email.split('@')[1]
            # if domain not in allowedDomains:
            #     raise APIException400({
            #         'success':'False',
            #         'meseage':'un-identified domain name',
            #     })
            user_qs = RegisteredUser.objects.filter(user__email__iexact=email)
            if user_qs.exists():
                raise APIException400({
                    'success':'False',
                    'message':'User with this email is already registered. Please login to continue.',
                })

# 'background', 'experience','category', 'declaration',
        # if user_type=='2':
        #     if not background or background=='':
        #         raise APIException400({
        #             'success':'False',
        #             'message':'background is required',
        #         })
        #     else:
        #         bg_queryset=Background.objects.filter(id=background)
        #         if not bg_queryset:
        #             raise APIException400({
        #                 'success':'False',
        #                 'message':'please provide valid background id',
        #             })
        #
        #     if not experience or experience=='':
        #         raise APIException400({
        #             'success':'False',
        #             'message':'experience is required',
        #         })
        #     if not category or category=="":
        #         raise APIException400({
        #             'success':'False',
        #             'message':'category is required',
        #         })
        #     else:
        #         ct_queryset=Category.objects.filter(id=category)
        #         if not ct_queryset:
        #             raise APIException400({
        #                 'success':'False',
        #                 'message':'please provide valid category id',
        #             })
        #
        #     if not declaration or declaration=='':
        #         raise APIException400({
        #             'success':'False',
        #             'message':'declaration file is required',
        #         })
        #     if not about_me or about_me=='':
        #         raise APIException400({
        #             'success':'False',
        #             'message':'about me is required',
        #         })

        if not password or password=='':
            raise APIException400({
                'success':'False',
                'message':'password is required',
            })

        if not device_type or device_type=='':
            raise APIException400({
                'success':'False',
                'message':'device_type is required',
            })


# mobile validation
        if mob.isdigit():
            user_qs=RegisteredUser.objects.filter(mobile__iexact=mob)
            if user_qs.exists():
                raise APIException400({
                    'success':'False',
                    'message':'This mobile number already exists. Please login to continue.',
                })
        else:
            if login_type in ('2','3'):
                mob='000000000'
            else:
                raise APIException400({
                    'success':'False',
                    'message':'Please provide a valid number only',
                })
        if len(password)<8:
            raise APIException400({
                'success':"False",
                'message':'Password must be at least 8 characters',
            })
# device type varification
        if device_type not in ['1','2','3']:
            raise APIException400({
                'success':'False',
                'message':'Please enter correct format of device_type',
            })

        data['email']=email
        data['mobile']=mob
        data['country_code']=country_code
        data['password']=password
        return data

    def create(self, validated_data):
        social_id = ''
# 'background', 'experience','category', 'declaration',
        name = validated_data['name']
        country_code = validated_data['country_code']
        mobile = validated_data['mobile']

        # background = validated_data['background']
        # if background:
        #     background=Background.objects.filter(id=background).first()
        # experience = validated_data['experience']
        # category = validated_data['category']
        # if category:
        #     category=Category.objects.filter(id=category).first()
        # declaration = self.context['request'].FILES.get('declaration')
        # about_me = validated_data['about_me']

        email = validated_data['email']
        password = validated_data['password']
        user_type = validated_data['user_type']

        first_name=name.split(' ')[0]
        last_name=' '.join(name.split(' ')[1:])
        username=''

        # if user_type=='1':
        #     username = email.split('@')[0]
        # else:
        #     username = country_code+mobile

        # if user_type=='1':
        #     user_obj = User(
        #         username = username,
        #         email = email,
        #         first_name=first_name,
        #         last_name=last_name,
        #     )
        # if user_type=='2':
        #     user_obj = User(
        #         username = username,
        #         first_name=first_name,
        #         last_name=last_name,
        #     )
        print('============================')
        print(email)
        print(mobile)
        user_obj = User(
            username = email.split('@')[0]+mobile,
            email = email,
            first_name=first_name,
            last_name=last_name,
        )

        user_obj.set_password(password)
        user_obj.save()


        device_type = validated_data['device_type']
        device_token = validated_data['device_token']
        login_type = validated_data['login_type']
        if login_type in ('2','3'):
            social_id = validated_data['social_id']
        is_approved=False

# 'background', 'experience','category', 'declaration',
        # if user_type=='1':
        #     ruser_obj = RegisteredUser(
        #         name=name,
        #         country_code=country_code,
        #         mobile=mobile,
        #         login_type = login_type,
        #         social_id = social_id,
        #         device_type = device_type,
        #         device_token = device_token,
        #         user_type = user_type,
        #         user = user_obj,
        #     )
        # if user_type=='2':
        #     ruser_obj = RegisteredUser(
        #         name=name,
        #         country_code=country_code,
        #         mobile=mobile,
        #         background=background,
        #         experience=experience,
        #         category=category,
        #         declaration=declaration,
        #         about_me=about_me,
        #         login_type = login_type,
        #         social_id = social_id,
        #         device_type = device_type,
        #         device_token = device_token,
        #         user_type = user_type,
        #         user = user_obj,
        #     )
        if social_id:
            ruser_obj = RegisteredUser(
                name=name,
                country_code=country_code,
                mobile=mobile,
                login_type = login_type,
                social_id = social_id,
                device_type = device_type,
                device_token = device_token,
                user_type = user_type,
                user = user_obj,
                is_email_verified=True,
                is_mobile_verified=True,
                is_approved=is_approved,
            )
        else:
            ruser_obj = RegisteredUser(
                name=name,
                country_code=country_code,
                mobile=mobile,
                login_type = login_type,
                social_id = social_id,
                device_type = device_type,
                device_token = device_token,
                user_type = user_type,
                user = user_obj,
                is_approved=is_approved,
            )
        ruser_obj.save()

        validated_data['token']=''
        if login_type in ('2','3') and user_type=='1':
            payload = jwt_payload_handler(user_obj)
            token = jwt_encode_handler(payload)
            token = 'JWT '+token
            validated_data['token'] = token

        validated_data['u_id'] = ruser_obj.id
        validated_data['created_on'] = ruser_obj.created_on
#******************************************************************************
        r_obj=RegisteredUser.objects.filter(user=user_obj).first()
        if r_obj.about_me:
            validated_data['is_profile_created']='True'
        else:
            validated_data['is_profile_created']='False'

        t_is_approved='True' if ruser_obj.is_approved else 'False'
        validated_data['is_approved']=t_is_approved

        if ruser_obj.is_mobile_verified:
            print('inside True***********************************')
            validated_data['is_mobile_verified']='True'
        else:
            validated_data['is_mobile_verified']='False'
        if ruser_obj.is_email_verified:
            validated_data['is_email_verified']='True'
        else:
            validated_data['is_email_verified']='False'
#*******************************************************************************
        validated_data['u_id'] = ruser_obj.id
        validated_data['created'] = ruser_obj.created_on

        print(validated_data['is_mobile_verified'])
        return validated_data
class LoginSerializer(serializers.ModelSerializer):
    name=serializers.CharField(read_only=True)
    email=serializers.CharField(read_only=True)
    country_code=serializers.CharField(allow_blank=True)
    mobile = serializers.CharField(allow_blank=True)
    password = serializers.CharField(allow_blank=True,write_only=True,label='Password',style={'input_type':'password'})
    device_type  = serializers.CharField(allow_blank=True)
    device_token = serializers.CharField(allow_blank=True)
    user_type = serializers.CharField(allow_blank=True)

    u_id = serializers.CharField(read_only=True)
    is_email_verified=serializers.CharField(allow_blank=True,read_only=True)
    is_mobile_verified=serializers.CharField(allow_blank=True,read_only=True)
    is_profile_created = serializers.CharField(read_only=True)
    is_approved = serializers.CharField(read_only=True)
    login_type = serializers.CharField(read_only=True)

    token = serializers.CharField(allow_blank=True,read_only=True)
    message = serializers.CharField(allow_blank=True, read_only=True)
    success = serializers.CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = ('u_id','name','country_code','email','is_email_verified','is_mobile_verified',
        'is_profile_created','is_approved','login_type',
        'mobile','password','device_type','device_token','user_type','token','message','success')

    def validate(self,data):
        mobile = data['mobile']
        password = data['password']
        device_token = data['device_token']
        device_type = data['device_type']
        user_type = data['user_type']

        if not mobile or mobile=='':
            raise APIException400({
                'success':'False',
                'message':'mobile is required',
            })

        if not password or password=='':
            raise APIException400({
                'success':'False',
                'message':'password is required',
            })

        if not device_type or device_type=='':
            raise APIException400({
                'success':'False',
                'message':'device_type is required',
            })
        if not user_type or user_type=='':
            raise APIException400({
                'success':'False',
                'message':'user_type is required',
            })

        ruser=RegisteredUser.objects.filter(mobile__iexact=mobile)
        user_obj=''
        if ruser.exists() and ruser.count()==1:
            ruser_obj=ruser.first()
            user_obj=ruser_obj.user
            # if ruser_obj.is_mobile_verified==False:
            #     raise APIException400({
            #         'success':'False',
            #         'message':'This mobile is not verified',
            #     })
        else:
            raise APIException400({
                'success':'False',
                'message':'This mobile number is not registered.',
            })

# password Validation
        if len(password)<8:
            raise APIException400({
                'success':"False",
                'message':'Password must be at least 8 characters',
            })

# device type varification
        if device_type not in ['1','2','3']:
            raise APIException400({
                'success':'False',
                'message':'Please enter correct format of device_type',
            })
        if user_type not in ['1','2']:
            raise APIException400({
                'success':'False',
                'message':'Please enter correct format of user_type',
            })

        if user_obj:
            if not user_obj.check_password(password):
                raise APIException400({
                    'success':'False',
                    'message':'Invalid credentials',
                })

            # if not user_obj.is_active:
            #     raise APIException400({
            #         'success':'False',
            #         'message':'Your account is not active. Pending admin approval.',
            #     })
            if ruser_obj.user_type != user_type:
                ruser_obj.has_dual_account=True
                ruser_obj.save()
                # raise APIException400({
                #     'success':'False',
                #     'message':'You are not authorised to login with this user type',
                # })
#-------------------------------------------------------------------------------
        ruser = RegisteredUser.objects.filter(user__id=user_obj.id)
        ruser = ruser.first()
        ruser_obj.device_type = device_type
        ruser_obj.device_token = device_token
        ruser_obj.save()

        if not user_obj.is_active:
            raise APIException400({
                'success':'False',
                'message':'Your account has been blocked by admin. Please contact admin.',
            })

        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        token = 'JWT '+token
        data['token']=token

        if user_type=='1' and ruser.is_mobile_verified==False:
            data['token']=''
        if user_type=='2'  and ruser.is_email_verified==False and ruser.is_mobile_verified==False:
            data['token']=''
        if user_type=='2' and ruser.is_approved==False:
            data['token']=''

        data['u_id']=ruser.id
        data['name']=ruser.name
        data['country_code']=ruser.country_code
        data['mobile']=ruser.mobile

        data['is_profile_created']='False'
        if ruser.about_me:
            data['is_profile_created']='True'

        data['is_approved']=ruser.is_approved
        data['is_email_verified']=ruser.is_email_verified
        data['is_mobile_verified']=ruser.is_mobile_verified
        data['login_type']=ruser.login_type
#-------------------------------------------------------------------------------
        # payload = jwt_payload_handler(user_obj)
        # token = jwt_encode_handler(payload)
        # data['token']=token
        # data['name']=user_obj.first_name
        # if user_obj.last_name:
        #     data['name']=user_obj.first_name+' '+user_obj.last_name
        return data
class ChangePasswordAfterSignInSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(allow_blank=True,required=True)
    newPassword = serializers.CharField(allow_blank=True,required=True)
    confPassword = serializers.CharField(allow_blank=True,required=True)

    def validate_oldPassword(self, password):
        if not password or password=='':
            raise APIException400({
                'success':'False',
                'message':'Old password is required'
            })
        if len(password) < 8:
            raise APIException400({
                'success':"False",
                'message':'Old password must be at least 8 characters',
            })
        return password
    def validate_newPassword(self, password):
        if not password or password=='':
            raise APIException400({
                'success':'False',
                'message':'New password is required'
            })
        if len(password) < 8:
            raise APIException400({
                'success':"False",
                'message':'New password must be at least 8 characters',
            })
        return password
    def validate_confPassword(self, password):
        if not password or password=='':
            raise APIException400({
                'success':'False',
                'message':'Confirm password is required',
            })
        if len(password) < 8:
            raise APIException400({
                'success':"False",
                'message':'Confirm password must be at least 8 characters',
            })
        return password
class ChangePasswordAfterVerificationSerializer(serializers.Serializer):
    newPassword = serializers.CharField(allow_blank=True,required=True)
    confPassword = serializers.CharField(allow_blank=True,required=True)

    def validate_newPassword(self, password):
        if not password or password=='':
            raise APIException400({
                'success':'False',
                'message':'New password is required'
            })
        if len(password) < 8:
            raise APIException400({
                'success':"False",
                'message':'New password must be at least 8 characters',
            })
        return password
    def validate_confPassword(self, password):
        if not password or password=='':
            raise APIException400({
                'success':'False',
                'message':'Confirm password is required',
            })
        if len(password) < 8:
            raise APIException400({
                'success':"False",
                'message':'Confirm password must be at least 8 characters',
            })
        return password

class UserProfileDetailSerializer(serializers.ModelSerializer):
    email=serializers.CharField(read_only=True)
    class Meta:
        model=RegisteredUser
        fields=['profile_image','name','email','age','country_code','mobile',
        'alt_mobile_country_code','alt_mobile','gender','profession','building_num',
        'locality','landmark','city','country','postal_code','user_type',
        'background','experience','category','declaration','about_me']

class UserProfileUpdateSerializer(serializers.Serializer):
    profile_image = serializers.ImageField(required=False)
    name = serializers.CharField(max_length=100, allow_blank=True)
    email = serializers.CharField(max_length=100, allow_blank=True)
    age = serializers.CharField(max_length=3, allow_blank=True,)
    country_code = serializers.CharField(max_length=10, allow_blank=True)
    mobile = serializers.CharField(max_length=10, allow_blank=True,error_messages={"max_length": "Please enter a valid mobile number"})
    alt_mobile_country_code = serializers.CharField(max_length=10, allow_blank=True)
    alt_mobile = serializers.CharField(max_length=10, allow_blank=True,error_messages={"max_length": "Please enter a valid alt mobile number"})
    gender = serializers.CharField(max_length=2,allow_blank=True,)
    profession = serializers.CharField(max_length=30,allow_blank=True)
    building_num = serializers.CharField(max_length=100,allow_blank=True)
    locality = serializers.CharField(max_length=200,allow_blank=True)
    landmark = serializers.CharField(max_length=100,allow_blank=True)
    city = serializers.CharField(max_length=50,allow_blank=True)
    country = serializers.CharField(max_length=50,allow_blank=True)
    postal_code = serializers.CharField(max_length=20,allow_blank=True)
# 'background', 'experience','category', 'declaration', 'about_me',


    class Meta:
        model = RegisteredUser
        fields = ('profile_image','name','email','age','country_code','mobile',
        'alt_mobile_country_code','alt_mobile','gender','profession','building_num',
        'locality','landmark','city','country','postal_code')

    def validate(self,data):
        name = data['name']
        email = data['email']
        age = data['age']
        country_code = data['country_code']
        mobile = data['mobile']
        alt_mobile_country_code = data['alt_mobile_country_code']
        alt_mobile = data['alt_mobile']
        gender = data['gender']
        profession = data['profession']
        building_num = data['building_num']
        locality = data['locality']
        landmark = data['landmark']
        city = data['city']
        country = data['country']
        postal_code = data['postal_code']



# fields = ('profile_image','name','email','age','country_code','mobile',
# 'alt_mobile_country_code','alt_mobile','gender','profession','building_num',
# 'locality','landmark','city','country','postal_code')

        if not email or email=='':
            raise APIException400({
                'success':'False',
                'message':'email is required'
            })
        if not country_code or country_code=='':
            raise APIException400({
                'success':'False',
                'message':'country_code is required'
            })
        if not mobile or mobile=='':
            raise APIException400({
                'success':'False',
                'message':'mobile is required'
            })

        if len(mobile)<8:
            raise APIException400({
                'success':'False',
                'message':'Not a valid mobile number'
            })

        if alt_mobile_country_code or alt_mobile:
            if not alt_mobile or alt_mobile=='':
                raise APIException400({
                    'success':'False',
                    'message':'alt_mobile is required'
                })
            if not alt_mobile_country_code or alt_mobile_country_code=='':
                raise APIException400({
                    'success':'False',
                    'message':'alt_mobile_country_code is required'
                })
            if len(alt_mobile)<8:
                raise APIException400({
                    'success':'False',
                    'message':'not a valid alt_mobile'
                })

        allowedDomains = [
        "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
        "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
        "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",
        "email.com", "games.com" , "gmx.net", "hush.com", "hushmail.com", "icloud.com", "inbox.com",
        "lavabit.com", "love.com" , "outlook.com", "pobox.com", "rocketmail.com",
        "safe-mail.net", "wow.com", "ygm.com" , "ymail.com", "zoho.com", "fastmail.fm",
        "yandex.com","iname.com"
        ]

        if '@' not in email:
            raise APIException400({
                'success':'False',
                'message':'Email is not valid',
            })
        else:
            domain = email.split('@')[1]
            if domain not in allowedDomains:
                raise APIException400({
                    'success':'False',
                    'message':'Not a valid domain',
                })
        if gender:
            if gender not in ('1','2'):
                raise APIException400({
                    'success':'False',
                    'message':'gender not valid',
                })

        ###############################################################


        return data

    def create(self, validated_data):
        user = self.context['request'].user
        ruser = RegisteredUser.objects.filter(user=user).first()

        pimage = self.context['request'].FILES.get('profile_image')
        first_name = validated_data['name'].split(' ')[0]
        last_name=' '.join(validated_data['name'].split(' ')[1:])

        name=validated_data['name']
        email=validated_data['email']
        country_code=validated_data['country_code']
        mobile=validated_data['mobile']
        alt_mobile_country_code=validated_data['alt_mobile_country_code']
        alt_mobile=validated_data['alt_mobile']
        gender=validated_data['gender']
        profession=validated_data['profession']
        building_num=validated_data['building_num']
        locality=validated_data['locality']
        landmark=validated_data['landmark']
        city=validated_data['city']
        country=validated_data['country']
        postal_code=validated_data['postal_code']

# fields = ('profile_image','name','email','age','country_code','mobile',
# 'alt_mobile_country_code','alt_mobile','gender','profession','building_num',
# 'locality','landmark','city','country','postal_code')
        # user.username=email.split('@')[0]
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.save()

        # if ruser.user_type==1:
        ruser.name = name
        ruser.profile_image = pimage
        ruser.country_code = country_code
        ruser.mobile = mobile
        ruser.alt_mobile_country_code=alt_mobile_country_code
        ruser.alt_mobile=alt_mobile
        ruser.gender=gender
        ruser.profession=profession
        ruser.building_num=building_num
        ruser.locality=locality
        ruser.landmark=landmark
        ruser.city=city
        ruser.country=country
        ruser.postal_code=postal_code



# fields = ('profile_image','name','email','age','country_code','mobile',
# 'alt_mobile_country_code','alt_mobile','gender','profession','building_num',
# 'locality','landmark','city','country','postal_code')
        ruser.save()

        # validated_data['profile_image'] = ruser.profile_image
        # validated_data['name'] = ruser.name
        # validated_data['country_code'] = ruser.country_code
        # validated_data['mobile'] = ruser.mobile
        # validated_data['email'] = user.email

        return validated_data

class NewUserProfileUpdateSerializer(serializers.Serializer):
    profile_image = serializers.ImageField(required=False)
    name = serializers.CharField(max_length=100, allow_blank=True)
    email = serializers.CharField(max_length=100, allow_blank=True)
    age = serializers.CharField(max_length=3, allow_blank=True,)
    country_code = serializers.CharField(max_length=10, allow_blank=True)
    mobile = serializers.CharField(max_length=10, allow_blank=True,error_messages={"max_length": "Please enter a valid mobile number"})
    alt_mobile_country_code = serializers.CharField(max_length=10, allow_blank=True)
    alt_mobile = serializers.CharField(max_length=10, allow_blank=True,error_messages={"max_length": "Please enter a valid alt mobile number"})
    gender = serializers.CharField(max_length=2,allow_blank=True,)
    profession = serializers.CharField(max_length=30,allow_blank=True)
    building_num = serializers.CharField(max_length=100,allow_blank=True)
    locality = serializers.CharField(max_length=200,allow_blank=True)
    landmark = serializers.CharField(max_length=100,allow_blank=True)
    city = serializers.CharField(max_length=50,allow_blank=True)
    country = serializers.CharField(max_length=50,allow_blank=True)
    postal_code = serializers.CharField(max_length=20,allow_blank=True)
# 'background', 'experience','category', 'declaration', 'about_me',
    background = serializers.CharField(allow_blank=True)
    experience = serializers.CharField(allow_blank=True)
    category = serializers.CharField(allow_blank=True)
    declaration = serializers.FileField(required=False,)
    about_me = serializers.CharField(allow_blank=True)
    payment = serializers.CharField()

    class Meta:
        model = RegisteredUser
        fields = ('profile_image','name','email','age','country_code','mobile',
        'alt_mobile_country_code','alt_mobile','gender','profession','building_num',
        'locality','landmark','city','country','postal_code',
        'background','experience','category','declaration','about_me','payment')

    def validate(self,data):
        name = data['name']
        email = data['email']
        age = data['age']
        country_code = data['country_code']
        mobile = data['mobile']
        alt_mobile_country_code = data['alt_mobile_country_code']
        alt_mobile = data['alt_mobile']
        gender = data['gender']
        profession = data['profession']
        building_num = data['building_num']
        locality = data['locality']
        landmark = data['landmark']
        city = data['city']
        country = data['country']
        postal_code = data['postal_code']

        background=data['background']
        experience=data['experience']
        category=data['category']
        declaration = self.context['request'].FILES.get('declaration')
        about_me=data['about_me']
        payment = data['payment']

# fields = ('profile_image','name','email','age','country_code','mobile',
# 'alt_mobile_country_code','alt_mobile','gender','profession','building_num',
# 'locality','landmark','city','country','postal_code')

        if not email or email=='':
            raise APIException400({
                'success':'False',
                'message':'email is required'
            })
        if not country_code or country_code=='':
            raise APIException400({
                'success':'False',
                'message':'country_code is required'
            })
        if not mobile or mobile=='':
            raise APIException400({
                'success':'False',
                'message':'mobile is required'
            })

        if len(mobile)<8:
            raise APIException400({
                'success':'False',
                'message':'Not a valid mobile number'
            })

        if alt_mobile_country_code or alt_mobile:
            if not alt_mobile or alt_mobile=='':
                raise APIException400({
                    'success':'False',
                    'message':'alt_mobile is required'
                })
            if not alt_mobile_country_code or alt_mobile_country_code=='':
                raise APIException400({
                    'success':'False',
                    'message':'alt_mobile_country_code is required'
                })
            if len(alt_mobile)<8:
                raise APIException400({
                    'success':'False',
                    'message':'not a valid alt_mobile'
                })

        allowedDomains = [
        "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
        "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
        "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",
        "email.com", "games.com" , "gmx.net", "hush.com", "hushmail.com", "icloud.com", "inbox.com",
        "lavabit.com", "love.com" , "outlook.com", "pobox.com", "rocketmail.com",
        "safe-mail.net", "wow.com", "ygm.com" , "ymail.com", "zoho.com", "fastmail.fm",
        "yandex.com","iname.com"
        ]

        if '@' not in email:
            raise APIException400({
                'success':'False',
                'message':'Email is not valid',
            })
        else:
            domain = email.split('@')[1]
            # if domain not in allowedDomains:
            #     raise APIException400({
            #         'success':'False',
            #         'message':'Not a valid domain',
            #     })
        if gender:
            if gender not in ('1','2'):
                raise APIException400({
                    'success':'False',
                    'message':'gender not valid',
                })

        ###############################################################
        ruser_obj=self.context['ruser']
        user_obj=ruser_obj.user
        # ruser_obj=RegisteredUser.objects.filter(user=user_obj).first()
        if ruser_obj.user_type=='2' or ruser_obj.has_dual_account==True:
            if not background or background=='':
                raise APIException400({
                    'success':'False',
                    'message':'background is required',
                })
            else:
                bg_queryset=Background.objects.filter(id=background)
                if not bg_queryset:
                    raise APIException400({
                        'success':'False',
                        'message':'please provide valid background id',
                    })

            if not experience or experience=='':
                raise APIException400({
                    'success':'False',
                    'message':'experience is required',
                })
            if not category or category=="":
                raise APIException400({
                    'success':'False',
                    'message':'category is required',
                })
            else:
                ct_queryset=Category.objects.filter(id=category)
                if not ct_queryset:
                    raise APIException400({
                        'success':'False',
                        'message':'please provide valid category id',
                    })

            # if not declaration or declaration=='':
            #     raise APIException400({
            #         'success':'False',
            #         'message':'declaration file is required',
            #     })
            if not about_me or about_me=='':
                raise APIException400({
                    'success':'False',
                    'message':'about me is required',
                })

        # tempuser = self.context['request'].user
        # tempruser = RegisteredUser.objects.filter(user=tempuser).first()

        return data

    def create(self, validated_data):
        ruser = self.context['ruser']
        user = ruser.user
        # ruser = RegisteredUser.objects.filter(user=user).first()

        pimage = self.context['request'].FILES.get('profile_image')
        first_name = validated_data['name'].split(' ')[0]
        last_name=' '.join(validated_data['name'].split(' ')[1:])

        name=validated_data['name']
        email=validated_data['email']
        country_code=validated_data['country_code']
        mobile=validated_data['mobile']
        alt_mobile_country_code=validated_data['alt_mobile_country_code']
        alt_mobile=validated_data['alt_mobile']
        gender=validated_data['gender']
        profession=validated_data['profession']
        building_num=validated_data['building_num']
        locality=validated_data['locality']
        landmark=validated_data['landmark']
        city=validated_data['city']
        country=validated_data['country']
        postal_code=validated_data['postal_code']
        payment = validated_data['payment']

        background = validated_data['background']
        if background:
            background=Background.objects.filter(id=background).first()
        experience = validated_data['experience']
        category = validated_data['category']
        if category:
            category=Category.objects.filter(id=category).first()
        declaration = self.context['request'].FILES.get('declaration')
        about_me = validated_data['about_me']

# fields = ('profile_image','name','email','age','country_code','mobile',
# 'alt_mobile_country_code','alt_mobile','gender','profession','building_num',
# 'locality','landmark','city','country','postal_code')
        # user.username=email.split('@')[0]
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.save()

        if ruser.user_type=='1':
            ruser.name = name
            ruser.profile_image = pimage
            ruser.country_code = country_code
            ruser.mobile = mobile
            ruser.alt_mobile_country_code=alt_mobile_country_code
            ruser.alt_mobile=alt_mobile
            ruser.gender=gender
            ruser.profession=profession
            ruser.building_num=building_num
            ruser.locality=locality
            ruser.landmark=landmark
            ruser.city=city
            ruser.country=country
            ruser.postal_code=postal_code
        print('*************************************************')
        print(type(ruser.has_dual_account))
        if ruser.user_type=='2' or ruser.has_dual_account==True:
            print('--------inside-----------------')
            ruser.name = name
            ruser.profile_image = pimage
            ruser.country_code = country_code
            ruser.mobile = mobile
            ruser.alt_mobile_country_code=alt_mobile_country_code
            ruser.alt_mobile=alt_mobile
            ruser.gender=gender
            ruser.profession=profession
            ruser.building_num=building_num
            ruser.locality=locality
            ruser.landmark=landmark
            ruser.city=city
            ruser.country=country
            ruser.postal_code=postal_code

            ruser.background=background
            ruser.experience=experience
            ruser.category=category
            ruser.declaration=declaration
            ruser.about_me=about_me
            ruser.payment =payment
            ruser.is_profile_created=True

# fields = ('profile_image','name','email','age','country_code','mobile',
# 'alt_mobile_country_code','alt_mobile','gender','profession','building_num',
# 'locality','landmark','city','country','postal_code')
        ruser.save()
        validated_data['profile_image']=""
        validated_data['declaration']=""
        if ruser.profile_image:
            validated_data['profile_image'] = ruser.profile_image
        if ruser.declaration:
            validated_data['declaration'] = ruser.declaration
        # validated_data['name'] = ruser.name
        # validated_data['country_code'] = ruser.country_code
        # validated_data['mobile'] = ruser.mobile
        # validated_data['email'] = user.email

        return validated_data
