import json
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import  ListCreateAPIView
from register.serializers import AddressSerializer, ApplyProjectAndProjectSerializer, ApplyProjectSerializer, ChangePasswordSerializer, ClientCreationSerializer, FreelancerDetailsSerializer, FreelancerUpdateSerializer, GetClientProjectsSerializer, GetUnassingedProjectSerializer, GetUserSerializer, PaymentStatusSerializer, ProjectAssignSerializer, ProjectCreationSerializer, ProjectFileSerializer, ProjectStatusSerializer, SendPasswordResetEmailSerializer, SendUserVerificationSerializer, UpdateUserSerializer, UserPasswordUpdateSerializer, UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, FreelancerCreationSerializer, VerifyUserEmailSerializer,AppliedFreelancerSerializer
from django.contrib.auth import authenticate, login, logout
from register.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
from register.models import  ApplyProject, Client, Freelancer, PaymentStatus, ProjectFile, ProjectStatus, ProjectsAssigned
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from register.models import User, Projects
from django.utils import timezone
import logging
import os
from django.utils.functional import empty
from django.db.models import Q


logger = logging.getLogger(__name__)


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
           user_id = user.id
           if(user.user_type == "client"):
                client_instance, created = Client.objects.get_or_create(user=user)
                print("client_instance", client_instance)
                print("instance", created)
           return Response({"token":token, 'msg': "User Registration Sucessfull", "user_id": user_id }, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self,request,format=None):
        
        print('the request is ', request)
        print('the request data is ', request.data)
        serializer = UserLoginSerializer(data=request.data)
        # IF USER IS VERIFIED 
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            is_Verified = serializer.data.get('is_verified')
            # user_type  = serializer.data.get('user_type')
            # created_at  = serializer.data.get('created_at')
            print("data is verfied:",is_Verified)
            user = authenticate(email=email,password=password)
            # print("the user is ", user)
            if user is not None:
                # IF USER IS VERIFIED 
                print("check if verified : ",serializer.data.get('is_verified'))
                if serializer.data.get('is_verified'):
                    # The signal is typically triggered by login() function from django.contrib.auth.
                    login(request, user)  # Add this line to trigger the signal
                    token = get_tokens_for_user(user)
                    user_type = user.user_type  # Fetch user_type from user object
                    user_id = user.id 
                    # created_at = user.created_at  # Fetch created_at from user object
                    return Response({'token': token, 'msg': "User Login Sucessfull😎", 'user_type': user_type,"user_id" : user_id}, status.HTTP_202_ACCEPTED)
                else:
                    return Response({'msg' : "User not verified"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'errors' : {'non_field_errors' : ['Email or Password not Valid']}}, status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)  
    
    
    
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        user = request.user

        serializer = UserProfileSerializer(request.user)
        # response_data = {
        #     # 'msg': f'The profile details of the user with user id {user.id} is : ',
        #     # 'id': user.id,
        #     # 'email': user.email,
        #     # 'name': f'{user.firstname} {user.lastname}',
        #     'data': serializer.data,
        # }
        return Response({"msg": serializer.data},status=status.HTTP_200_OK)
                
class ChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def post(self,request,format=None):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'user':user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': "Password Changed"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_401_UNAUTHORIZED)
    
class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"msg" : "Password Reset Link was sent to your provided Email. Please Check your Email. 😊"}, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordUpdateView(APIView):
    renderer_classes = [UserRenderer]
    
    '''
        def get(self,uid,token):
        uid token
        if valid
        return render('changepassword.html',daat)
    '''
    def get(self,request, uid, token):
        print(request)
        print(uid)
        print(token)
        
        context = {
            'id' : uid, 
            'token' : token, 
            'url' : 'http://localhost:8000' if os.getenv('PR') == 'False' else 'https://gokap.onrender.com'
        }
        
        return render(request= request,template_name='reset_password.html', context=context)
        # return redirect('/reset_password.html')
    
    def post(self, request, uid, token ,format=None):
        serializer = UserPasswordUpdateSerializer(context = {'id':uid, 'token': token},data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"msg " : "Password is Updated in the Database. 😊"}, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# It is a class-based view that allows you to define the behavior and logic for handling different HTTP methods (GET, POST, PUT, PATCH, DELETE, etc.) in your API.
class FreelancerCreationView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        
        # Print the user that comes with the request as token
        print("user", request.user)
        print("user", request.user.id)
        # Print the data that comes with the request from the form 
        print("data", request.data)
        
        # Along with the request comes the user(there is permission_classes) and the data 
        '''
        The issue you're facing is likely due to the fact that request.data is an immutable QueryDict object when dealing with form data. To modify it, you need to convert it to a mutable dictionary first.
        '''
        data = request.data.copy()
        user = request.user.id
        data['user'] = user
        print("the final data is : ", data)
        
        # This line creates an instance of the FreelancerSerializer class. 
        # It takes the request.data as the data to be serialized.
        serialized = FreelancerCreationSerializer(data=data)
        
        # This line checks whether the data provided to the serializer is valid according to the serializer's validation rules. The is_valid() method is a DRF method that triggers the validation process.
        if serialized.is_valid():
            # If the data is valid, this line saves the data to the database.
            serialized.save()
            return Response({"msg": "Freelancer Created", "serialized_data": serialized.data}, status=status.HTTP_201_CREATED)
        return Response({"msg": "Freelancer isn't created","serialized_errors" : serialized.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    # get all the frelancers
    def get(self, request):
     
        # Get the queryset 
        freelancers = Freelancer.objects.all()
        
        # The many parameter is a boolean flag used to indicate whether the serializer should be used to serialize a single instance (many=False) or multiple instances (many=True)
        serialized = FreelancerCreationSerializer(freelancers, many=True)
        
        return Response({'serialized_data': serialized.data})
        
# Get Freelancer by Id
class FreelancerDetails(APIView):
    
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):   
      user  = request.user
      
      try:
          freelancer_details= Freelancer.objects.get(user=user.id)
      except Freelancer.DoesNotExist:
          return Response({'error': 'Freelancer not found'}, status=status.HTTP_404_NOT_FOUND)

      serialized= FreelancerDetailsSerializer(freelancer_details)
      return Response({'serialized_data': serialized.data}, status=status.HTTP_200_OK)

           
class ClientCreationView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serialized = ClientCreationSerializer(data=request.data, context={'request': request})
        if serialized.is_valid():
            # Get or create a client instance
            client_instance, created = Client.objects.get_or_create(user=request.user)
            print("client_instance", client_instance)
            print("instance", created)
            
            # Associate the project with the client
            serialized.save(client=client_instance)
            
            return Response({"msg":"Client Created!", "details": serialized.data}, status=status.HTTP_201_CREATED)
        return Response({'msg': "Client can't be created 🙏🏿", "errors": serialized.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request, *args, **kwargs):
        
        clients = Client.objects.all()
        serialized = ClientCreationSerializer(clients, many=True)
        return Response({'data': serialized.data})
        
        
class ProjectCreationView(APIView):
    
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def post(self,request,*args, **kwargs):
        data = request.data
        data['client'] = request.user.id
        print(data)
        serialized = ProjectCreationSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"msg":"Project Created!", "details": serialized.data}, status=status.HTTP_201_CREATED)
        return Response({'msg': "Project can't be created", "errors": serialized.errors}, status=status.HTTP_400_BAD_REQUEST)
    
   
class ProjectUpdateView(APIView):
    
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    # get object
    def get_object(self, project_id):
        try:    
            return Projects.objects.get(pk=project_id)
        except Projects.DoesNotExist:
            return None
        
    
    def put(self,request,project_id, *args, **kwargs):
        
        # get object
        project = self.get_object(project_id)
        if project is None:
            return Response({"msg": "Project is not found"}, status=status.HTTP_404_NOT_FOUND) 
        
        serialized = ProjectCreationSerializer(project, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response({"msg":"Project Updated!", "details": serialized.data}, status=status.HTTP_201_CREATED)
        return Response({'msg': "Project can't be Updated 🙏🏿", "errors": serialized.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request, project_id, *args, **kwargs):
        project = self.get_object(project_id)
        if project is None:
            return Response({'msg': "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProjectCreationSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Project Updated!", "details": serializer.data}, status=status.HTTP_200_OK)
        return Response({'msg': "Project can't be Updated 🙏🏿", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class SendUserVerificationLinkView(APIView): 
    
    renderer_classes = [UserRenderer] 
    
    def post(self, request):
        serialized = SendUserVerificationSerializer(data=request.data)
        if serialized.is_valid():
            return Response({"msg" : "Email Verification Link have been sent"}, status=status.HTTP_200_OK)
        return Response({'msg': "Error", "errors": serialized.errors}, status=status.HTTP_400_BAD_REQUEST)
    
# Verify UserEmail
class VerifyUserEmailView(APIView):
    
    renderer_classes = [UserRenderer]
    
    def get(self, request,*args, **kwargs):
        string = str(request)  
        id = string.split("/")
        uid = smart_str(urlsafe_base64_decode(id[4]))
        context = {
            'id' : id[4], 
            'token' : id[5]
        }
        # print(context)
        request.data['id'] = uid
        request.data['firstname'] = 'rupesh'

        serialized = VerifyUserEmailSerializer(data=request.data, context=context)
        
        if serialized.is_valid():
            return render(request=request,template_name='verified.html')            

        return render(request=request, template_name='404.html')
        
from rest_framework import mixins
from rest_framework import generics

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
        print('the request is : ', request)
        print('the args is : ', args)
        print('the kwargs is : ', kwargs)
        # print('the kwargs['pk'] is :', kwargs['pk'])
        # print('the kwargs['int'] is :', kwargs['int'])
        print('the pk is : ', kwargs.get('pk'))
        if 'pk' in kwargs:
            return self.retrieve(request, kwargs['pk'])
        else:
            return self.list(request)
    
    def post(self, request, *args, **kwargs):
        return self.create(request,*args, **kwargs)
    
    
    # def put(self, request, *args, **kwargs):
    #     return self.put(request,*args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        print(f"the use {kwargs['pk']} is going to be deleted")
        print(f"the use {kwargs.get('pk')} is going to be deleted")
        response =  super().destroy(request, *args, **kwargs)
        print("the response is : ", response)
        response.data['msg'] = "User Deletion Sucessfull"
        return Response({"msg":"User deleted success"},status=status.HTTP_200_OK)
    
# class UpdateUserView(mixins.UpdateModelMixin, generics.GenericAPIView):

#     renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]
    
#     queryset = User.objects.all()
#     serializer_class = UpdateUserSerializer
    
#     def put(self, request):
#         # print("put ", args)
#         return self.update(request, pk=1)

# Update User
class UpdateUserView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    # get the user
    def patch(self, request):
        user_queryset = User.objects.get(id=request.user.id)
        print("user_queryset", user_queryset)
        last_updated = user_queryset.updated_at  # Assuming you have a field to track the last update time
        current_time = timezone.now()
        
        if last_updated and (current_time - last_updated).days < 7:
            return Response({'error': f'Your name was updated on : { last_updated }You can only update your name only after a week.'}, status=status.HTTP_400_BAD_REQUEST)
        
        print(request.data)
        user_queryset.firstname = request.data['firstname']
        user_queryset.lastname = request.data['lastname']
        user_queryset.last_updated = current_time  # Update the last updated time
        user_queryset.save()
        
        return Response({'msg': 'User Update Sucessfull'}, status=status.HTTP_200_OK)
    
# Get all the projecct of the specific client
class GetClientProjects(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        user = request.user
        id = user.id
        # get all the projects created by the user with given id. 
        queryset = Projects.objects.filter(client_id=id)
        serializer = GetClientProjectsSerializer(queryset, many=True)

        return Response(serializer.data)
    
class ProjectAssignView(APIView):
    
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ProjectAssignSerializer(data=request.data)
        if serializer.is_valid():
            
            assigned = serializer.validated_data['assigned']
            
            if assigned:
                # raise ValueError("Project is Already Assigned. ")
                return Response({"error": "The Project is already assigned. "})
            
            frelancer_id = serializer.validated_data['frelancer_id']         
            project_id = serializer.validated_data['project_id']  
            print("the project id is : " , project_id)     
            print("the project id is : " , project_id.id)    
            print(type(project_id)) 
            obj = ProjectsAssigned.objects.create(frelancer_id=frelancer_id, project_id=project_id)
            project_data = ProjectAssignSerializer(obj)
            if obj is None:
                raise ValueError("Error Assigning Project")
            else:
                project = Projects.objects.get(id=project_id.id)
                project.project_assigned_status = True
                project.save()
                return Response({'msg': "Project Assigned", 'data':project_data.data})
        else:
            return Response({'error':serializer.errors})
        
    
    def delete(self, request):
        
        serializer = ProjectAssignSerializer(data=request.data)
        if serializer.is_valid():
            print("the delete serialiser is ", serializer.data)
            project_id = serializer.data['project_id']
            print(project_id, "this is project id ")
            if ProjectsAssigned.objects.get(project_id=project_id).exists():
            # if queryset.exists():
            #     queryset.delete()
                ProjectsAssigned.objects.get(project_id=project_id).delete()
                return JsonResponse({'msg':"UnAssigned"}, status=201)
            else:
                return JsonResponse({'msg':"Already  deleted"}, status=400)
        else:
            return JsonResponse({"errors":  serializer.errors, 'msg':'project doesnt existes.'}, status=400)
            

# API to get the unassigned projects for freelancers
class GetUnassingedProjects(APIView):
    
    renderer_classes = [UserRenderer]
    
    def get(self, request):
        # Fetch all projects that are not assigned
        unassigned_projects = Projects.objects.filter(project_assigned_status=False).order_by('-created_at')
        serializer = GetUnassingedProjectSerializer(unassigned_projects, many=True)
        return Response({'data': serializer.data, 'msg': "Unassigned Projects Retrieved Successfully"}, status=status.HTTP_200_OK)

# Delete Project
class DeleteUnassignedProject(APIView):
    
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, **kwargs):
        
        project_id = kwargs['project_id']
        
        # check if the project with the id exists
        if Projects.objects.filter(id=project_id):
        
            project = Projects.objects.get(id = project_id)
            if project.project_assigned_status == False:
                delete_status = project.delete()
                print("delete_status", delete_status)
                return Response({"msg": "Project deleted sucessfully"}, status=status.HTTP_200_OK )
        
            return Response({"msg": "Project is Assigned"}, status=status.HTTP_400_BAD_REQUEST )  
        else:
            return Response({"msg": "Project Does Not Exists"}, status=status.HTTP_400_BAD_REQUEST )  

# Logout View             
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, format=None):
#         try:
#             refresh_token = request.data["refresh"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response({"msg": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response({"msg": request, "refresh": request.data['refresh'], "error": str(e),}, status=status.HTTP_400_BAD_REQUEST)
   
'''
This logout view does the following:

It uses the IsAuthenticated permission class to ensure only authenticated users can access this view.
It expects a POST request with a "refresh_token" in the request data.
It blacklists the refresh token to invalidate it, preventing its future use.
It calls Django's logout() function to log out the user on the server side.
It returns a success message if the logout is successful, or an error message if something goes wrong.
'''
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()

#             logout(request)

#             return Response({"success": "User logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             auth_header = request.headers.get('Authorization')
#             if not auth_header or not auth_header.startswith('Bearer '):
#                 return Response({"error": "Invalid token format"}, status=status.HTTP_400_BAD_REQUEST)

#             token = auth_header.split(' ')[1]
#             AccessToken(token)  # This will raise an error if the token is invalid

#             # Perform any additional logout actions here
#             logout(request)

#             return Response({"success": "User logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
#         except TokenError as e:
#             return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return Response({"error": "Invalid token format"}, status=status.HTTP_400_BAD_REQUEST)

            token = auth_header.split(' ')[1]
            token_obj = AccessToken(token)
            
            # Add token to blacklist
            outstanding_token = OutstandingToken.objects.get(token=token)
            BlacklistedToken.objects.create(token=outstanding_token)

            return Response({"success": "User logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# Apply Projects
class ApplyProjectView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print("id", request.user.id)
        data = request.data
        data['frelancer_id'] = request.user.id
        serializer = ApplyProjectSerializer(data= data)
        print("data is",data)
        project = Projects.objects.get(pk=data['project_id'])
        if serializer.is_valid():
            serializer.save()
            project.applied_count += 1
            project.save()
            return Response({"msg": "Project Applied Sucess"}, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_404_NOT_FOUND)

# the api to get all the applied projects of a particular freelancer based on their token
class GetAppliedProject(APIView):
    
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # 1. get the user 
        user = request.user
        
        try:
            freelancer = Freelancer.objects.get(user=user)
            # get applied projects from the table of this user
            # applied_projects = ApplyProject.objects.filter(frelancer_id=freelancer)
            # applied_projects = ApplyProject.objects.select_related('project_id').all()
            applied_projects = ApplyProject.objects.filter(frelancer_id=freelancer).select_related('project_id').all()
            print(applied_projects.values_list())
            try:
                serialized = ApplyProjectAndProjectSerializer(applied_projects, many=True)
                return Response({'serialized_data': serialized.data}, status=status.HTTP_200_OK)
            except Exception as e: 
                return Response({'error_message' : str(e)})
        except Exception as e:
            return Response({'error': str(e),}, status=status.HTTP_404_NOT_FOUND)
    
    
# API's to populate ProjectStatus
class ProjectStatusView(generics.ListCreateAPIView):
    
    queryset = ProjectStatus.objects.all()
    serializer_class = ProjectStatusSerializer
    
# API's to populate ProjectStatus
class PaymentStatusView(generics.ListCreateAPIView):
    
    queryset = PaymentStatus.objects.all()
    serializer_class = PaymentStatusSerializer
    
    
# API Database for holding project screenshots, doc and pdf files
class ProjectFileView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        project_files = ProjectFile.objects.filter(project_id=project_id)
        serializer = ProjectFileSerializer(project_files, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, project_id):
        data = request.data
        data['project'] = project_id
        serializer = ProjectFileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

# get the projects details by id
class GetProjectDetailsByIdView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes =  [ IsAuthenticated]
    
    def get(self, request,project_id):
        projects = get_object_or_404(Projects,pk=project_id)
        seralizer = ProjectCreationSerializer(projects)
        
        return Response({"serialized_data":seralizer.data})
        
# Update Freelancer View
class UpdateFreelancerView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        user = request.user
        data = request.data
        data['user'] = user.id
        freelancer = Freelancer.objects.get(user=user.id)
        queryset = FreelancerCreationSerializer(freelancer,data=data,partial=True)
        print("queryset",queryset)
        if queryset.is_valid():
            queryset.save()
            return Response({'msg':"success", 'data': queryset.data}, status=status.HTTP_200_OK)
        return Response({'error': queryset.errors}, status=status.HTTP_400_BAD_REQUEST)  
        
    def patch(self, request):
        pass

# Get Clinet Details by Id
class GetClientDetailsById(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, client_id):
        client = Client.objects.get(pk=client_id)
        user = User.objects.get(pk= client.pk)
        
        print(user.firstname)
        queryset = UserRegistrationSerializer(user)
        return Response({'serialized_data': queryset.data})
    
# Search API based on Freelancer Skills
class FreelancerSearchView(APIView):
    
    def get(self, request):
        skills = request.query_params.get('skills', '').lower().split(',')
        languages = request.query_params.get('languages', '').lower().split(',')
        profession = request.query_params.get('profession', '').lower()

        # Start with a base queryset
        queryset = Freelancer.objects.all()
        
        # This checks if the skills list is not empty and not just a list with an empty string. It ensures we only apply the filter if actual skills were provided in the query.
        if skills and skills != ['']:
            # This initializes an empty Q object. Q objects in Django are used to build complex database queries.
            skill_query = Q()
            for skill in skills:
                skill_query |= Q(skills__icontains=skill.strip())
                # skills__icontains is a Django lookup that checks if the skills field contains the given value, case-insensitive.
                # strip() removes any leading or trailing whitespace from the skill.
                # The |= operator is used to combine this new condition with the existing skill_query using OR logic.
            queryset = queryset.filter(skill_query)
            
            
        if languages and  languages != ['']:
            language_query = Q()
            for language in languages:
                language_query |= Q(languages__icontains=language.strip())
            queryset = queryset.filter(language_query)
            
        if profession : 
            queryset =  queryset.filter(profession__icontains=profession)
            
        # If no filters applied, return an error
        if not (skills or languages or profession):
            return Response({"error": "No search criteria provided"}, status=400)
        
        
        # Create a Q object for each skill
        # It uses __icontains for case-insensitive partial matching on all fields.
        # query = Q()
        # for skill in skills:
        #     query |= Q(skills__icontains=skill)

        print("Freelancer Queryset : ", queryset.query)
        serializer = FreelancerCreationSerializer(queryset, many=True)
        print("Serializer : ", serializer)
        return Response(serializer.data)

class PriceFilterView(APIView): 
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, price_start, price_end, n_applicant): 
        
        if(n_applicant < 0 and price_end > 0):
             queryset = Projects.objects.filter(project_price__range=(price_start,price_end))
             serialized = ProjectCreationSerializer(queryset, many=True)
             return Response({'serialized_data': serialized.data}, status=status.HTTP_201_CREATED)
        if(n_applicant >=0 and price_end > 0):
             queryset = Projects.objects.filter(applied_count__range=(0,n_applicant)  ,project_price__range=(price_start,price_end))
             serialized = ProjectCreationSerializer(queryset, many=True)
             return Response({'serialized_data': serialized.data}, status=status.HTTP_201_CREATED)
        if(price_end <= 0 and n_applicant >=0):
             queryset = Projects.objects.filter(applied_count__range=(0,n_applicant))
             serialized = ProjectCreationSerializer(queryset, many=True)
             return Response({'serialized_data': serialized.data}, status=status.HTTP_201_CREATED)
        if(price_end == 0 and n_applicant < 0):
            return Response({"error":"Invalid filter"},status=status.HTTP_400_BAD_REQUEST)  
            
class ProjectSearchView(APIView):
    renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        title = request.query_params.get('title', None)
        description = request.query_params.get('description', None)
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        min_applicants = request.query_params.get('min_applicants', None)
        max_applicants = request.query_params.get('max_applicants', None)

        queryset = Projects.objects.all()

        if title:
            queryset = queryset.filter(title__icontains=title)
        if description:
            queryset = queryset.filter(description__icontains=description)
        if min_price:
            queryset = queryset.filter(project_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(project_price__lte=max_price)
        if min_applicants:
            queryset = queryset.filter(applied_count__gte=min_applicants)
        if max_applicants:
            queryset = queryset.filter(applied_count__lte=max_applicants)

        if not (title or description or min_price or max_price or min_applicants or max_applicants):
            return Response({"error": "No search criteria provided"}, status=400)

        serialized = ProjectCreationSerializer(queryset, many=True)
        return Response({'serialized_data': serialized.data}, status=status.HTTP_200_OK)
       
# views for addresss
class AddressDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        address = request.user.address
        serializer = AddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
            return Response({"error" :  "The user has no address"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg" : "Address updated successfully", "data" : serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
    
        try: 
            address = request.user.address
            address.delete()
            print("user is : ", request.user)
            print("address is : ", request.user.address)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "Address deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# GET applied freelancers Freelancer details for any project_id
class AppliedFreelancersVeiw(APIView):
    
    def get(self,request,id):
        # get freelancers detail for specific project
        try:
            project_id = id
            # applied_project = ApplyProject.objects.filter(project_id=project_id)
            # print("applied_projcts", applied_project)
            applied_project_freelancer  = ApplyProject.objects.filter(project_id=project_id).select_related('frelancer_id')
            for i in applied_project_freelancer:
                
                print(i.frelancer_id.pk)
                
            applied_serialized = AppliedFreelancerSerializer(applied_project_freelancer,many=True)
            #Get freelancer id from the project
            # freelancers_ids = applied_project.values_list("frelancer_id",flat=True)
            # # print("applied freelancer Id ",freelancers_ids)
            # #Get detail for all freelancers 
            # freelancers_details = Freelancer.objects.filter(pk__in=freelancers_ids)
            # user_id = freelancers_details.values_list('user', flat=True)
            # print(type(freelancers_details))
            # print(freelancers_details)
            # print("Detail is",freelancers_details)
            # frelancer_user_ids = list(freelancers_details.values('user'))
            # print("frelancer user ids : ", frelancer_user_ids)   
            # print("frelancer user ids : ", type(frelancer_user_ids)) 
            # user_id = []
            # for user in frelancer_user_ids:
            #     # print('user is : ',  user['user'])
            #     user_id.append(user['user'])
                
            # print(user_id, ' : user id ')   
            # users = User.objects.filter(pk__in=user_id) 
            # print("users are : " ,users)
            # print(user.values())
            # print(user.get('user'))
            # print(user.get('firstname'))
            # user_serializer = UserRegistrationSerializer(users, many=True)
            # print("s datat " , user_serializer.data)
            
            # serialized = FreelancerDetailsSerializer(freelancers_details,many=True)
            # # serialized['user_details '] = user_serializer.data
            return Response({"serialized_data":applied_serialized.data})
        except Exception as e :
            return Response({"error":f"{e}"},status=status.HTTP_400_BAD_REQUEST)