from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import ChangePasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordUpdateSerializer, UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


# function to generate jwt access and refresh token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
# Create your views here.
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
           user = serializer.save()
           token = get_tokens_for_user(user)
           return Response({"token":token, 'msg': "User Registration Sucessfull🫡"}, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': "User Login Sucessfull😎"}, status.HTTP_202_ACCEPTED)
            else:
                return Response({'errors' : {'non_field_errors' : ['Email or Password not Valid']}}, status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)   
    
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        serializer = UserProfileSerializer(request.user)
        response_data = {
            'msg': f'The profile details of the user with user id {user.id} is : ',
            # 'id': user.id,
            # 'email': user.email,
            # 'name': f'{user.firstname} {user.lastname}',
            'data': serializer.data,
        }
        return Response(response_data,status=status.HTTP_200_OK)
                
class ChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def post(self,request,format=None):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'user':user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg ': "Password Changed!!! WOW 🙏🙏"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_401_UNAUTHORIZED)
    
class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"msg " : "Password Reset Link was sent to your provided Email. Please Check your Email. 😊"}, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordUpdateView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request, uid, token ,format=None):
        serializer = UserPasswordUpdateSerializer(context = {'id':uid, 'token': token},data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"msg " : "Password is Updated in the Database. 😊"}, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


            