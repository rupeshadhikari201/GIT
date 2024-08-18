from django.shortcuts import render
from rest_framework.views import APIView
from register.models import User
from common.serializer import UserRegistrationSerializer
from freelancer.serializer import GetDetailsOfFrelancersSerializer
from project.models import Projects
from project.serializer import ProjectCreationSerializer
from register.renderers import UserRenderer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializer import ClientCreationSerializer
from .models import Client
from client import serializer
from rest_framework.response import Response

# Create your views here.
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
        return Response({"error": serialized.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request, *args, **kwargs):
        
        clients = Client.objects.all()
        serialized = ClientCreationSerializer(clients, many=True)
        return Response({'data': serialized.data})
    
# Get Client Details by Id
class GetClientDetailsById(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, client_id):
        client = Client.objects.get(pk=client_id)
        user = User.objects.get(pk= client.pk)
        
        print(user.firstname)
        queryset = UserRegistrationSerializer(user)
        return Response({'serialized_data': queryset.data})
    
# Get all the Projects of the Specific Client
class GetClientProjects(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        user = request.user
        id = user.id
        # get all the projects created by the user with given id. 
        queryset = Projects.objects.filter(client_id=id)
        serialized = serializer.GetClientProjectsSerializer(queryset, many=True)

        return Response(serialized.data)

# Get User Details of a User Type Clients
class GetUserDetailsOfClients(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        clients_queryset = User.objects.filter(user_type="client")
        serialized = GetDetailsOfFrelancersSerializer(clients_queryset, many=True)
        return Response({"data": serialized.data}, status=status.HTTP_200_OK)
    
# api that return's clients project details by that client id
class GetClientProjectsDetailByCliendId(APIView):
    
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self,request,client_id):
        queryset = Projects.objects.filter(client_id=client_id)
        serialized = ProjectCreationSerializer(queryset, many=True)
        return Response({"data":serialized.data})