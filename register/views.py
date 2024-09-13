from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from project.models import ProjectStatus
from client.models import Client
from rest_framework import mixins
from rest_framework import generics
from register.serializer import AddressSerializer,ChangePasswordSerializer,  GetUserSerializer, SendPasswordResetEmailSerializer, SendUserVerificationSerializer, UpdateUserSerializer, UserPasswordUpdateSerializer, UserLoginSerializer, UserProfileSerializer,  VerifyUserEmailSerializer
from common.serializer import UserRegistrationSerializer
from django.contrib.auth import authenticate, login, logout
from register.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import  render
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from register.models import User
from django.utils import timezone
import logging
import os
from django.utils.functional import empty
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


logger = logging.getLogger(__name__)


# function to generate jwt access and refresh token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
# API to Register User
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        #changing to lowercase
        request.data['email'] = request.data['email'].lower() if request.data and request.data['email'] else ""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
           user = serializer.save()
           token = get_tokens_for_user(user)
           user_id = user.id
           if(user.user_type == "client"):
                client_instance, created = Client.objects.get_or_create(user=user)
           return Response({"token":token, 'msg': "User Registration Sucessfull", "user_id": user_id }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API to Login User
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self,request):
        
        serialized = UserLoginSerializer(data=request.data)
        # IF USER IS VERIFIED 
        if serialized.is_valid(raise_exception=True):
            email = serialized.data.get('email')
            password = serialized.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                # IF USER IS VERIFIED 
                if serialized.data.get('is_verified'):
                    # The signal is typically triggered by login() function from django.contrib.auth.
                    # Add this line to trigger the signal
                    login(request, user)  
                    token = get_tokens_for_user(user)
                    # Fetch user_type ans user_id from user object
                    user_type = user.user_type  
                    user_id = user.id 
                    # created_at = user.created_at  # Fetch created_at from user object
                    return Response({'token': token, 'msg': "User Login Sucessfull", 'user_type': user_type,"user_id" : user_id}, status.HTTP_202_ACCEPTED)
                else:
                    return Response({'errors' : "User not verified"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'errors' : {'non_field_errors' : 'Email or Password not Valid'}}, status.HTTP_404_NOT_FOUND)
        else:
            return Response(serialized.errors, status.HTTP_400_BAD_REQUEST)  
    
# API to View Profie of Currently LoggedIn User
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serialized = UserProfileSerializer(request.user)
        return Response({"serialized_data": serialized.data},status=status.HTTP_200_OK)
    
# API to Change Password of the User        
class ChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self,request,format=None):
        # The user is send as context to the ChangePassword Serializer
        user = request.user
        serialized = ChangePasswordSerializer(data=request.data, context={'user':user})
        if serialized.is_valid(raise_exception=True):
            return Response({'msg': "Password Changed"}, status=status.HTTP_200_OK)
        return Response(serialized.errors, status.HTTP_401_UNAUTHORIZED)

# API to Send Password Reset Email   
class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    # This allows for flexibility in serving different data formats (like JSON, XML, etc.) to different clients.
    # When format=None, Django REST Framework will attempt to determine the appropriate format based on the Accept header in the client's request.
    def post(self, request, format=None):
        serialized = SendPasswordResetEmailSerializer(data=request.data)
        if serialized.is_valid(raise_exception=True):
            return Response({"msg" : "Password Reset Link was sent to your provided Email. Please Check your Email."}, status.HTTP_200_OK)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

# API to Update Password         
class UserPasswordUpdateView(APIView):
    renderer_classes = [UserRenderer]

    def get(self,request, uid, token):
        context = {
            'id' : uid,
            'token' : token,
            'url' : 'http://localhost:8000' if os.getenv('PR') == 'False' else 'https://gokap.onrender.com'
        }
        
        return render(request=request,template_name='reset_password.html', context=context)
    
    def post(self, request, uid, token ,format=None):
        serialized = UserPasswordUpdateSerializer(context = {'id':uid, 'token': token},data=request.data)
        if serialized.is_valid(raise_exception=True):
            return Response({"msg" : "Password is Updated in the Database."}, status.HTTP_200_OK)
        return Response( serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
# API to Send User Verification Link
class SendUserVerificationLinkView(APIView): 
    
    renderer_classes = [UserRenderer] 
    
    def post(self, request):
        serialized = SendUserVerificationSerializer(data=request.data)
        if serialized.is_valid():
            return Response({"msg" : "Email Verification Link have been sent"}, status=status.HTTP_200_OK)
        return Response( serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
# API to Verify User Email
class VerifyUserEmailView(APIView):

    renderer_classes = [UserRenderer]
    
    def get(self, request, *args, **kwargs):
        string = str(request)  
        id = string.split("/")
        uid = smart_str(urlsafe_base64_decode(id[4]))
        
        context = {
            'id' : id[4],
            'token' : id[5]
        }

        request.data['id'] = uid
        serialized = VerifyUserEmailSerializer(data=request.data, context=context)

        if serialized.is_valid():
            return render(request=request,template_name='verified.html')            
        return render(request=request, template_name='404.html')

# API to Get All User, Details of a User if id is Provide
class GetUserView(mixins.ListModelMixin,
              mixins.CreateModelMixin,
              mixins.RetrieveModelMixin,
              mixins.UpdateModelMixin,
              mixins.DestroyModelMixin,
              generics.GenericAPIView
              ):

    queryset = User.objects.all()
    serializer_class = GetUserSerializer
    def get(self, request, *args, **kwargs):
        
        # Check if 'pk' is in kwargs to determine whether to retrieve a single user or all users
        if 'pk' in kwargs:
            return self.retrieve(request, kwargs['pk'])
        else:
            return self.list(request)
 
# API To Update User Details (First Name and Last Name)
class UpdateUserView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    # get the user
    def patch(self, request):
        user_queryset = User.objects.get(id=request.user.id)
        # Get the last UpdatedTime
        last_updated = user_queryset.updated_at  
        current_time = timezone.now()

        if last_updated and (current_time - last_updated).days < 7:
            return Response({'errors': f'Your name was updated on : { last_updated } \n You can only update your name only after a week.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_queryset.firstname = request.data['firstname']
        user_queryset.lastname = request.data['lastname']
        user_queryset.last_updated = current_time  # Update the last updated time
        user_queryset.save()
        return Response({'msg': 'User Update Sucessfull'}, status=status.HTTP_200_OK)
    
# API TO Logout User
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return Response({"errors": "Invalid token format"}, status=status.HTTP_400_BAD_REQUEST)

            token = auth_header.split(' ')[1]
            # Add token to blacklist
            outstanding_token = OutstandingToken.objects.get(token=token)
            BlacklistedToken.objects.create(token=outstanding_token)

            return Response({"success": "User logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# API to get, post, update and Delete Address
class AddressDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            address = request.user.address
            serializer = AddressSerializer(address)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'errors' : str(e)},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        address = None
        try:
            address = request.user.address if request.user.address is not empty else None
        except Exception as e:
            return Response({"errors" :  "The user has no address"},status=status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"serialized_data" : serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):

        try:
            address = request.user.address
            address.delete()
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "Address deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class UserProfileByIdView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            query_set = User.objects.get(pk=user_id)
            serializer = UserProfileSerializer(query_set)
            return Response({"serialized_data": serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({'errors':str(e)})







