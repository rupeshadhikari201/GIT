from django.utils.encoding import smart_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import serializers
from freelancer.serializer import FreelancerDetailsSerializer
from project.models import ApplyProject
from freelancer.models import Freelancer
from register.models import  Notification, User, Address
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404
import os

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     cnfpassword = serializers.CharField(style={'input_type' : 'password'},write_only=True)
#     class Meta:
#         model = User
#         fields = ['firstname','lastname','email','password', 'cnfpassword',"user_type", "id"]
#         extra_kwargs = {
#             'password' : {'write_only': True}
#         }
        
#     # Validate Password and cnfpassword
#     def validate(self, attrs):
#         password = attrs.get('password')
#         cnfpassword = attrs.get('cnfpassword')
#         if password != cnfpassword:
#             raise serializers.ValidationError("Password and Confirm password must be same!")
#         return attrs
    
#     # Create Method
#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    
    class Meta:
        model = User
        fields = ['email','password', 'is_verified','id']
        
    def validate(self, attrs):
        email = attrs['email']
        try:
            email = str(email).lower()
            user = User.objects.get(email=email)
            attrs['is_verified'] = user.is_verified
            attrs['id'] = user.id
            return attrs
        
        except User.DoesNotExist:
            raise serializers.ValidationError("User doesn't Exists")
            
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['firstname','lastname','email',"user_type"]
        # fields = '__all__'
        exclude = ['password']
        
        
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    cnfpassword = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['password', 'cnfpassword']
        
    def validate(self, attrs):
        password = attrs.get('password')
        cnfpassword = attrs.get('cnfpassword')
        user = self.context.get('user')
        if len(password) < 6:
            raise serializers.ValidationError("password length should be atleast 6")
        if password != cnfpassword:
            raise serializers.ValidationError("Password and Confirm  Password is not Equal")
        user.set_password(password)
        user.save()
        return attrs
    
class SendPasswordResetEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    
    class Meta:
        model = User
        fields = ['email']
    
    def validate(self, attrs):
        # Check if the user with the provided email exists in our database or 
        email = attrs.get('email')
        if User.objects.filter(email =email).exists():
            #if exists then send reset link
            # 1. get the user
            user = User.objects.get(email=email)
            # 2. get the user id, and encode it for privacy purpose
            uid = urlsafe_base64_encode(force_bytes(user.id)) 
            # 3. generate the token for that user
            token = PasswordResetTokenGenerator().make_token(user)
            # 4. generate the reset link
            baseUrl = 'http://localhost:8000' if os.getenv('PR') == 'False' else 'https://gokap.onrender.com'
            link = baseUrl + "/api/user/user-password-update/" + uid +"/" + token
            subject = 'Password Reset'
            body  = f'Dear, {user.firstname} please reset the email using following link. {link}'
            send_from = "gokap@gokapinnotech.com"
            send_to = [user.email]
            send_mail(subject,body,send_from,send_to)
            return attrs
        else: 
            raise serializers.ValidationError("The email is not Registered. Please register Yourself.")
        
class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, style={'input_type=': 'password'}, write_only=True)
    cnfpassword = serializers.CharField(max_length=255, style={'input_type=': 'password'}, write_only=True)
    
    class Meta:
        model =User
        fields = ['password', 'cnfpassword']
    
    def validate(self, attrs):
        password = attrs.get('password')
        cnfpassword = attrs.get('cnfpassword')
        uid = self.context.get('id')
        token = self.context.get('token')
        if password!=cnfpassword:
            raise serializers.ValidationError(" Password and Confirm password are not same. Password can't be updated.")
        else:
            # 1. get the id and decode it to sting
            uid = smart_str(urlsafe_base64_decode(uid))
            # 2. get the token and match with if the token generated for that user is same or not
            # each user is assigned a unique token by PRTG, 
            # so chekc if the this token which we got from url matches with the user or not
            user = User.objects.get(id=uid)
          
            token_generator_object = PasswordResetTokenGenerator()
            if not token_generator_object.check_token(user,token):
                raise serializers.ValidationError("The token is Invalid or Expired.")
            # 3. else save the password
            user.set_password(password)
            user.save()
        return attrs
    

class FreelancerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freelancer
        fields = '__all__'
        
        
class SendUserVerificationSerializer(serializers.ModelSerializer):
    
    # serialize the email Field
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email']
    
    
    def validate(self, attrs):
        # Check if the user with the provided email exists in our database or 
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            #if exists then send reset link
            # 1. get the user
            user = User.objects.get(email=email)
            # 2. get the user id, and encode it for privacy purpose
            uid = urlsafe_base64_encode(force_bytes(user.id)) 
            # 3. generate the token for that user
            token = PasswordResetTokenGenerator().make_token(user) 
            # 4. generate the reset link
            baseUrl = 'http://localhost:8000' if os.getenv('PR') == 'False' else 'https://gokap.onrender.com'
            link =  baseUrl + "/api/user/validate-email/" + uid +"/" + token
            
            subject = 'Verify Your Email'
            body  = f'Dear, {user.firstname} please verify the email using following link. {link}'
            send_from = "gokap@gokapinnotech.com"
            send_to = [user.email]
            send_mail(subject,body,send_from,send_to)
            return attrs
        else: 
            raise serializers.ValidationError("The email is not Registered. Please register Yourself.")

class VerifyUserEmailSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        self.id = context.get('id')
        self.token = context.get('token')
        super().__init__(*args, **kwargs)
        
        print(context)
    class Meta:
        model =User
        fields = ['id']
 
    def validate(self, attrs):
       
        # 1. get the id and decode it to sting
        uid = smart_str(urlsafe_base64_decode(self.id))
        # 2. get the token and match with if the token generated for that user is same or not
        # each user is assigned a unique token by PRTG, 
        # so chekc if the this token which we got from url matches with the user or not
        user = User.objects.get(id=uid)
        token_generator_object = PasswordResetTokenGenerator()
        if not token_generator_object.check_token(user,self.token):
            raise serializers.ValidationError("The token is Invalid or Expired.")
            # return render(request=request, template_name='404.html')
        # 3. else save the verify user
        user.is_verified=True
        user.save()
        return attrs
    


class GetUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        db_table = 'register_user'
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        model= User
        fields = '__all__'
        
class UpdateUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= User
        fields = ['firstname','lastname']
        
    
    
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'read', 'timestamp']
        read_only_fields = ['id', 'timestamp']  
        
   
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class AppliedFreelancerSerializer(serializers.ModelSerializer):
    frelancer_id = FreelancerDetailsSerializer()
    class Meta:
        model = ApplyProject
        fields = '__all__'      
 


        
