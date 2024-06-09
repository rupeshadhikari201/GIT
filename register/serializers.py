import ast
from urllib import response
from rest_framework import status
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import serializers
from register.models import ApplyProject, Client, Notification, PaymentStatus, ProjectFile, ProjectStatus, Projects, User, Freelancer, ProjectsAssigned
from register.utils import Util
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404
import os



class UserRegistrationSerializer(serializers.ModelSerializer):
    cnfpassword = serializers.CharField(style={'input_type' : 'password'},write_only=True)
    class Meta:
        model = User
        fields = ['firstname','lastname','email','password', 'cnfpassword',"user_type", "id"]
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
        fields = ['email','password', 'is_verified','id']
        
    def validate(self, attrs):
        print("the attrs from validate is :", attrs['email'])
        email = attrs['email']
        try:
            
            user = User.objects.get(email=email)
            user2 = User.objects.filter(email=email)
            print("the user is : ", user)
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
            print("Encoded Uid is: ", uid)
            # 3. generate the token for that user
            token = PasswordResetTokenGenerator().make_token(user)
            print("Password Reset Token : ", token)
            # 4. generate the reset link
            baseUrl = 'http://localhost:8000' if os.getenv('PR') == 'False' else 'https://gokap.onrender.com'
            print(os.getenv('PR'))
            link = baseUrl + "/api/user/user-password-update/" + uid +"/" + token
            print("Password Reset Link : ", link)
            print("The target email is : ", user.email)
            subject = 'Password Reset'
            body  = f'Dear, {user.firstname} please reset the email using following link. {link}'
            send_from = "gokap@gokapinnotech.com"
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
            print("Actual token is :",token)
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
    

class FreelancerCreationSerializer(serializers.ModelSerializer):
    
    skills = serializers.ListField(child=serializers.CharField())
    languages = serializers.ListField(child=serializers.CharField())
    
    class Meta:
        model = Freelancer
        fields = ['user', 'profession', 'skills','languages', 'reason_to_join','where_did_you_heard', 'resume','bio']
    
    '''
    The "to_internal_value" method is part of Django REST framework's serializer validation process. It is responsible for converting the incoming primitive data types (typically JSON) into native Python data types and validating them. This method is usually overridden to perform custom deserialization and validation.
    '''
    def to_internal_value(self, data):
        if 'skills' in data and isinstance(data['skills'], str):
            data['skills'] = data['skills'].strip('][').split(', ')
            
        if 'languages' in data and isinstance(data['languages'], str):
            data['languages'] = data['languages'].strip('][').split(', ')
        
        # After converting the skills and languages fields to lists, the method calls super().to_internal_value(data) to leverage the default behavior provided by ModelSerializer. 
        return super().to_internal_value(data)
    
    '''
    The validate method in a Django REST framework serializer is used to provide custom validation logic. The commented-out validate method you provided attempts to process the skills attribute, but it has some issues.
    '''
    def validate(self, attrs):
        # retrive the skills attribute from the attrs dictionary, which contains all the validated data
        skills = attrs.get('skills')
        
        # check if the skills is an instance of string
        if isinstance(skills, str):
            
            # The ast.literal_eval function safely evaluates a string containing a Python literal or container display (like a list, dictionary, or string) and converts it into an actual Python object. This line assumes that skils is a string representation of a list and attempts to convert it into a Python list.
            try:
                skills_list = ast.literal_eval(skills)
                
                if not isinstance(skills_list, list):
                    raise ValueError
            
            except (ValueError,SyntaxError):
                raise serializers.ValidationError({'skills': 'Invalid format for skills. Must be a list or a string representation of a list.'})
            
            attrs['skills'] = skills_list
            
        return attrs

class ClientCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['user']

    def validate_user(self, value):
        print("the value is : ", value)
        return value

    def create(self, validated_data):
        user_id = validated_data.pop('user')
        user = User.objects.get(id=user_id)
        client = Client.objects.create(user=user, **validated_data)
        return client
   
# class ClientCreationSerializer(serializers.ModelSerializer):
#     # user = User()?
    
#     class Meta:
#         model = Client
#         fields = ['user','projects_uploaded'] 
        
#     # def create(self, validated_data):
#     #     user_data = validated_data.pop('user')
#     #     user = User.objects.create(**user_data)
#     #     client = Client.objects.create(user=user, **validated_data)
#     #     return client
    
#     # def validate_user(self, value):
#     #     if not value.exists():
#     #         raise serializers.ValidationError("Invalid user ID. User does not exist.")
#     #     return value
    
#     # def validate_user(self, value):
#     #     try:
#     #         user = User.objects.get(pk=value)
#     #     except User.DoesNotExist:
#     #         raise serializers.ValidationError("Invalid user ID. User does not exist.")
#     #     return value
    
#     # Validate that the provided user object has a valid ID
#     # def validate_user(self, value):
#     #     if not isinstance(value, int):
#     #         raise serializers.ValidationError("Invalid user ID format.")
#     #     return value
    
#     def validate_user(self, value):
#         try:
#             # user_id = int(value)
#             user = User.objects.get(id=value)
#             print('kye the user is ', user)
#             return user
#         except (ValueError, User.DoesNotExist):
#             raise serializers.ValidationError("Invalid user ID format.")
        
class ProjectCreationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Projects
        fields = ['project_category', 'title','description', 'project_price', 'project_deadline','skills_required','client']
        
class SendUserVerificationSerializer(serializers.ModelSerializer):
    
    # serialize the email Field
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email']
    
    
    def validate(self, attrs):
        print("the type of attrs is     : ", type(attrs))
        print("the attrs of validate is : ", attrs)
        # Check if the user with the provided email exists in our database or 
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
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
            baseUrl = 'http://localhost:8000' if os.getenv('PR') == 'False' else 'https://gokap.onrender.com'
            link =  baseUrl + "/api/user/validate-email/" + uid +"/" + token
            print("Password Reset Link : ", link)
            print("The target email is : ", user.email)
              
            subject = 'Verify Your Email'
            body  = f'Dear, {user.firstname} please verify the email using following link. {link}'
            send_from = "gokap@gokapinnotech.com"
            send_to = [user.email]
            send_mail(subject,body,send_from,send_to)
            return attrs
        else: 
            raise serializers.ValidationError("The email is not Registered. Please register Yourself.😡😡😡")

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
  
        print("the is atrr :",attrs.items())
        print("this is new id and token : ",self.id, self.token)
       
        # 1. get the id and decode it to sting
        uid = smart_str(urlsafe_base64_decode(self.id))
        print("Actual User id is : ", uid)
        # 2. get the token and match with if the token generated for that user is same or not
        # each user is assigned a unique token by PRTG, 
        # so chekc if the this token which we got from url matches with the user or not
        user = User.objects.get(id=uid)
        print("The Actual User is : ", user)
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
        
        
class ProjectAssignSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProjectsAssigned
        fields = ['frelancer_id','project_id',]
        
    def validate(self, attrs):
        try:
            project = get_object_or_404(ProjectsAssigned,project_id= attrs.get('project_id'))
            
            if project is not None:
                attrs['assigned'] = True
            return attrs
        except:
            attrs['assigned'] = False
            return attrs
      
class GetClientProjectsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Projects
        fields = "__all__" 
         
class GetUnassingedProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Projects
        fields= '__all__'
    

class ApplyProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ApplyProject
        fields = '__all__'


# Project Status Serializer
class ProjectStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProjectStatus
        fields= '__all__'
        
# Payment Status Serializer
class PaymentStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PaymentStatus
        fields= '__all__'
        
# Project Profile File Serializer

class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = '__all__'
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'read', 'timestamp']
        read_only_fields = ['id', 'timestamp']  
        
   

        
    

    