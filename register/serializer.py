from django.utils.encoding import smart_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import serializers
from register.models import  User, Address
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os

# API Serializer to Register User  
class UserRegistrationSerializer(serializers.ModelSerializer):
    # cnfpassword = serializers.CharField(style={'input_type' : 'password'},write_only=True)
    # class Meta:
    #     model = User
    #     fields = ['firstname','lastname','email','password', 'cnfpassword',"user_type", "id"]
    #     extra_kwargs = {
    #         'password' : {'write_only': True}
    #     }
        
    # # Validate Password and cnfpassword
    # def validate(self, attrs):
    #     password = attrs.get('password')
    #     cnfpassword = attrs.get('cnfpassword')
    #     if password != cnfpassword:
    #         raise serializers.ValidationError("Password and Confirm password must be same!")
    #     return attrs
    
    # # Create Method
    # def create(self, validated_data):
    #     return User.objects.create_user(**validated_data)
    pass

# API Serializer to Login User  
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    
    class Meta:
        model = User
        fields = ['email','password', 'is_verified','id']
        
    def validate(self, attrs):
        email = attrs['email']
        try:
            user = User.objects.get(email=email)
            attrs['is_verified'] = user.is_verified
            attrs['id'] = user.pk
            return attrs
        
        except User.DoesNotExist:
            raise serializers.ValidationError("User doesn't Exists")
            
# API Serializer for User Profile   
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
    
# API Serializer to Change Password
class ChangePasswordSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    cnfpassword = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['password', 'cnfpassword']
        
    def validate(self, attrs):
        print("validate is called : ", attrs)
        password = attrs.get('password')
        cnfpassword = attrs.get('cnfpassword')
        if password != cnfpassword:
            raise serializers.ValidationError("Password and Confirm Password is not Equal")
        # we are getting user object from the ChangePasswordView, sent as context
        user = self.context.get('user')
        user.set_password(password)
        user.save()
        return False

# API Serializer to Send Password Reset Email     
class SendPasswordResetEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    
    class Meta:
        model = User
        fields = ['email']
    
    def validate(self, attrs):
        # Check if the user with the provided email exists in our database 
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # 2. Get the user id, and encode it using 'urlsafe_base64_encode
            uid = urlsafe_base64_encode(force_bytes(user.id)) 
            print("Encoded Uid is: ", uid)
            # 3. Generate the token for that user
            token = PasswordResetTokenGenerator().make_token(user)
            print("Password Reset Token : ", token)
            # 4. Generate the reset link
            baseUrl = 'http://localhost:8000' if os.getenv('PR') == 'False' else 'https://gokap.onrender.com'
            print(os.getenv('PR'))
            link = baseUrl + "/api/user/update_password/" + uid +"/" + token
            print("Password Reset Link : ", link)
            print("The target email is : ", user.email)
            subject = 'Password Reset'
            body  = f'Dear, {user.firstname} Please reset the email using following link. {link}'
            send_from = "gokap@gokapinnotech.com"
            send_to = [user.email]
            send_mail(subject,body,send_from,send_to)
            return attrs
        else: 
            raise serializers.ValidationError("The email is not Registered. Please register Yourself.")

# API Serializer to Update Password         
class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, style={'input_type=': 'password'}, write_only=True)
    cnfpassword = serializers.CharField(max_length=255, style={'input_type=': 'password'}, write_only=True)
    
    class Meta:
        model =User
        fields = ['password', 'cnfpassword']
    
    def validate(self, attrs):
        password = attrs.get('password')
        cnfpassword = attrs.get('cnfpassword')
        if password!=cnfpassword:
            raise serializers.ValidationError(" Password and Confirm password are not same. Password can't be updated.")
        else:
            uid = self.context.get('id')
            token = self.context.get('token')
            # 1. Get the uid and decode it to string
            uid = smart_str(urlsafe_base64_decode(uid))
            # 2. get the token and match with if the token generated for that user is same or not
            # NOTE: Each user is assigned a unique token by PRTG, 
            # So, check if this token which we got from url matches with the user's token or not
            user = User.objects.get(id=uid)
            print("The Actual User is : ", user)
            # Create an Objec of PasswordResetTokenGenerator Class
            token_generator_object = PasswordResetTokenGenerator()
            if not token_generator_object.check_token(user,token):
                raise serializers.ValidationError("The token is Invalid or Expired.")
            # 3. else save the new password
            user.set_password(password) 
            user.save()
        return attrs
    
# API Serializer to Send User Verification Link       
class SendUserVerificationSerializer(serializers.ModelSerializer):
    
    # serialize the email Field
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email']
    
    def validate(self, attrs):
        # Check if the user with the provided email exists in our database or 
        email = attrs.get('email')
        if email:
            email = email.lower()
        print(email)
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id)) 
            token = PasswordResetTokenGenerator().make_token(user) 
            # 4. generate the reset link
            baseUrl = 'http://localhost:8000' if os.getenv('PR') == 'False' else 'https://gokap.onrender.com'
            link =  baseUrl + "/api/user/verify_email/" + uid +"/" + token
            # Render HTML email template
            html_message = render_to_string('verification_email.html', {
                'user': user,
                'verification_link': link
            })

            # Create plain text version of the email
            plain_message = strip_tags(html_message)
            subject = 'Verify Your Email'
            body  = f"""
            Dear {user.firstname},
            Please verify your email address by clicking on the following link:
            {link}
            If you did not request this verification, please ignore this email.
            Best regards,
            Gokap Team.
            """
            send_from = "gokap@gokapinnotech.com"
            send_to = [user.email]
            send_mail(subject,body,send_from,send_to,html_message=html_message)
            return attrs
        else: 
            raise serializers.ValidationError("The email is not Registered. Please register Yourself.")

# API Serializer to VerifyUser    
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
    
# API Serializer Get All User, Details of a User if id is Provide, Update and Delete User
class GetUserSerializer(serializers.ModelSerializer):
    '''
    Non-Applicable Attributes for Serializers
        1. db_table
        2. managed              
        3. verbose_name
        4. verbose_name_plural
    These attributes belong in the Meta class of a Django model, not in a serializer.
    '''
    class Meta:
        model= User
        fields = '__all__'

# API to Update User's FirstName and LastName  
class UpdateUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= User
        fields = ['firstname','lastname']
      
# API Serializer to get, post, update and Delete Address
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


 


        
