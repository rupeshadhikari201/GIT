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
from rest_framework.pagination import PageNumberPagination
# API to Create Client
class ClientCreationView(APIView):
    
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serialized = ClientCreationSerializer(data=request.data, context={'request': request})
        if serialized.is_valid():
            # Get or create a client instance
            client_instance, created = Client.objects.get_or_create(user=request.user)
            # Associate the project with the client
            serialized.save(client=client_instance)
            return Response({"msg":"Client Created!", "serialized_data": serialized.data}, status=status.HTTP_200_OK)
        return Response({"errors": serialized.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request):
        
        clients = Client.objects.all()
        serialized = ClientCreationSerializer(clients, many=True)
        return Response({'serialized_data': serialized.data},status=status.HTTP_200_OK)
    
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
    
# Get all the Projects of the Specific Client (Currentl Authorized)
class GetClientProjects(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        user = request.user
        id = user.id
        # get all the projects created by the user with given id. 
        queryset = Projects.objects.filter(client=id)
        serialized = serializer.GetClientProjectsSerializer(queryset, many=True)

        return Response({'serialized_data':serialized.data},status=status.HTTP_200_OK)
class UserPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 100
# Get User Details of a all User whose user_type is 'client' (User Details of a Client)
class GetAllClient(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        clients_queryset = User.objects.filter(user_type="client")
        paginator = UserPagination()
        paginated_queryset = paginator.paginate_queryset(clients_queryset, request, view=self)
        serializer_instance = GetDetailsOfFrelancersSerializer(paginated_queryset, many=True)
        result = paginator.get_paginated_response(serializer_instance.data)
        return Response({"serialized_data":result.data},status=status.HTTP_200_OK)

class ClientSearchView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        name = request.query_params.get('name')
        email = request.query_params.get('email')
        queryset = User.objects.filter(user_type="client")
        if name:
            queryset = queryset.filter(firstname__icontains=name) | queryset.filter(lastname__icontains=name)
        if email:
            queryset = queryset.filter(email__icontains=email)

        if not queryset.exists():
            return Response({"message": "No matching client found"}, status=404)
        paginator = UserPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request, view=self)
        serializer_instance = GetDetailsOfFrelancersSerializer(paginated_queryset, many=True)
        result = paginator.get_paginated_response(serializer_instance.data)
        return Response({'serialized_data': result.data}, status=status.HTTP_200_OK)

class DeleteClient(APIView):
    def delete(self, request, id):
        try:
            user = User.objects.get(pk=id)
            if Projects.objects.filter(client_id=user.id).exists():
                return Response({'errors': 'Cannot delete user with active projects.'}, status=status.HTTP_400_BAD_REQUEST)
            user.delete()
            return Response({'message': 'User deleted successfully.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'errors': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
# Get Client's Project details by Client Id
class GetClientProjectsDetailByCliendId(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,client_id):
        queryset = Projects.objects.filter(client=client_id)
        serialized = ProjectCreationSerializer(queryset, many=True)
        return Response({"serialized_data":serialized.data})