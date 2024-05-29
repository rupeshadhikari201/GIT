from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from register.serializers import ChangePasswordSerializer, ClientCreationSerializer, GetClientProjectsSerializer, GetUnassingedProjectSerializer, GetUserSerializer, ProjectAssignSerializer, ProjectCreationSerializer, SendPasswordResetEmailSerializer, SendUserVerificationSerializer, UpdateUserSerializer, UserPasswordUpdateSerializer, UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, FreelancerCreationSerializer, VerifyUserEmailSerializer
from django.contrib.auth import authenticate
from register.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from register.models import  Client, Freelancer, ProjectsAssigned
from django.shortcuts import redirect, render
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from register.models import User, Projects

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
        
        # print('the reques is ', request)
        # print('the reques data is ', request.data)
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
                    token = get_tokens_for_user(user)
                    user_type = user.user_type  # Fetch user_type from user object
                    # created_at = user.created_at  # Fetch created_at from user object
                    return Response({'token': token, 'msg': "User Login Sucessfull😎", 'user_type': user_type}, status.HTTP_202_ACCEPTED)
                else:
                    return Response({'msg' : "User not verified. "}, status=status.HTTP_401_UNAUTHORIZED)
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
            'token' : token
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
    
    def post(self, request, format=None):
        # print("this is request to crete freelncer " , request)
        # print("this is the data for the request ", request.data)
        # This line creates an instance of the FreelancerSerializer class. It takes the request.data as the data to be serialized.
        serialized = FreelancerCreationSerializer(data=request.data)
        print("this is the serialized data ", serialized)
        
        # This line checks whether the data provided to the serializer is valid according to the serializer's validation rules. The is_valid() method is a DRF method that triggers the validation process.
        if serialized.is_valid():
            # If the data is valid, this line saves the data to the database.
            serialized.save()
            return Response({"msg": "Freelancer Created 😎", "result": serialized.data}, status=status.HTTP_201_CREATED)
        return Response({"msg": "Freelancer isn't created","erros" : serialized.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        freelancers = Freelancer.objects.all()
        print("the object of freelancer are : ", freelancers)
        # The many parameter is a boolean flag used to indicate whether the serializer should be used to serialize a single instance (many=False) or multiple instances (many=True
        serialized = FreelancerCreationSerializer(freelancers, many=True)
        
        return Response({'data': serialized.data})
        
    
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
    
    def post(self,request,*args, **kwargs):
        serialized = ProjectCreationSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response({"msg":"Project Created!", "details": serialized.data}, status=status.HTTP_201_CREATED)
        return Response({'msg': "Project can't be created 🙏🏿", "errors": serialized.errors}, status=status.HTTP_400_BAD_REQUEST)
    
   
class ProjectUpdateView(APIView):
    
    renderer_classes = [UserRenderer]
    
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
        return Response({'msg': "Error 🙏🏿", "errors": serialized.errors}, status=status.HTTP_400_BAD_REQUEST)
    
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
        return response;
    
class UpdateUserView(mixins.UpdateModelMixin, generics.GenericAPIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    
    def put(self, request):
        # print("put ", args)
        return self.update(request, pk=1)
    
    
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
        unassigned_projects = Projects.objects.filter(project_assigned_status=False)
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
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"msg": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
        
            


    
    