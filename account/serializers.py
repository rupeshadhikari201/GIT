from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import serializers
from account.models import User
from account.utils import Util
from django.core.mail import send_mail
from django.conf import settings

class UserRegistrationSerializer(serializers.ModelSerializer):
    cnfpassword = serializers.CharField(style={'input_type' : 'password'},write_only=True)
    class Meta:
        model = User
        fields = ['firstname','lastname','email','password', 'cnfpassword',]
        extra_kwargs = {
            'password' : {'write_only': True}
        }
        
    # Validate Password and cnfpassword
    def validate(self, attrs):
        password = attrs.get('password')
        cnfpassword = attrs.get('cnfpassword')
        if password != cnfpassword:
            raise serializers.ValidationError("Password and Confirm password must be same!!!!😂")
        return attrs
    
    # Create Method
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']
        

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['id','firstname','lastname','is_admin','email','created_at','updated_at']
        fields = '__all__'
        
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
        if password != cnfpassword:
            raise serializers.ValidationError("Password and Confirm  Passwors is not Equal.😡😡")
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
            print("Encoded Uid is: ", uid)
            # 3. generate the token for that user
            token = PasswordResetTokenGenerator().make_token(user)
            print("Password Reset Token : ", token)
            # 4. generate the reset link
            link = "https://localhost:3000/api/user/reset-password/" + uid +"/" + token
            print("Password Reset Link : ", link)
            print("The target email is : ", user.email)
            # SEND EMAIL
            # data = {
            #     'subject' : 'Password Reset',
            #     'body' : 'Please Click on this link to reset your  password.' + link,
            #     'to_email' : user.email,
                
            # }
            # Util.send_email(data)
            subject = 'Password Reset'
            body  = f'Dear, {user.firstname} please reset the email using following link. {link}'
            send_from = "21bcs11201@gmail.com"
            send_to = [user.email]
            send_mail(subject,body,send_from,send_to)
            return attrs
        else: 
            raise serializers.ValidationError("The email is not Registered. Please register Yourself.😡😡😡")
        
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
            raise serializers.ValidationError(" Password and Confirm password are not same. Password can't be updated. 🤐🤐🤐")
        else:
            # 1. get the id and decode it to sting
            uid = smart_str(urlsafe_base64_decode(uid))
            print("Actual User id is : ", uid)
            # 2. get the token and match with if the token generated for that user is same or not
            # each user is assigned a unique token by PRTG, 
            # so chekc if the this token which we got from url matches with the user or not
            user = User.objects.get(id=uid)
            print("The Actual User is : ", user)
            token_generator_object = PasswordResetTokenGenerator()
            if not token_generator_object.check_token(user,token):
                raise serializers.ValidationError("The token is Invalid or Expired.")
            # 3. else save the password
            user.set_password(password)
            user.save()
        return attrs