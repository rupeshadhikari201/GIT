import os
from django.http import JsonResponse
from rest_framework.response import Response
from freelancer.serializer import  ApplyedProjectAndFreelancerSerializer, GetDetailsOfFrelancersSerializer
from project.models import ApplyProject, Projects, ProjectsAssigned
from project.serializer import ProjectCreationSerializer
from register.models import User
from . import serializer
from rest_framework.views import APIView
from register.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.pagination import PageNumberPagination
# Create your views here.
class ProjectAssignView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    # To Assign a Project
    def post(self, request):
        serialized = serializer.ProjectAssignSerializer(data=request.data)
        if serialized.is_valid():
            freelancer = serialized.validated_data['freelancer']         
            project = serialized.validated_data['project']   
            obj = ProjectsAssigned.objects.create(freelancer=freelancer, project=project)
            project_data = serializer.ProjectAssignSerializer(obj)
            if obj is None:
                raise ValueError("Error Assigning Project")
            else:
                project = Projects.objects.get(id=project.id)
                project.project_assigned_status = True
                project.save()
                return Response({'msg': "Project Assigned", 'serialized_data':project_data.data},status=status.HTTP_200_OK)
        else:
            return Response({"errors":serialized.errors},status=status.HTTP_400_BAD_REQUEST)
        
    # To Unassign a Project 
    def delete(self, request):
        
        serialized = serializer.ProjectAssignSerializer(data=request.data)
        if serialized.is_valid():
            project_id = serialized.data['project_id']
            if ProjectsAssigned.objects.get(project_id=project_id).exists():
            
                ProjectsAssigned.objects.get(project_id=project_id).delete()
                return JsonResponse({'msg':"UnAssigned"}, status=201)
            else:
                return JsonResponse({'errors':"Already  deleted"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(serialized.errors, status=400)
 
# get all the project assigned to a frelancer using the frelancer id
class GetAssignedProjectUsingFrelancerID(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self,request, freelancer_id):
        try:
            project_ids_queryset = ProjectsAssigned.objects.filter(freelancer=freelancer_id)
            print(project_ids_queryset) 
            project_id_list = []
            for i in project_ids_queryset:
                project_id_list.append(i.project_id)
            project_queryset = Projects.objects.filter(id__in=project_id_list)
            serialized = ProjectCreationSerializer(project_queryset, many=True)
            return Response({"serialized_data":serialized.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"errors":str(e)},status=status.HTTP_400_BAD_REQUEST)
# get all the project assigned to a frelancer using the frelancer id
class GetAssignedFreelancerUsingProjectId(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self,request, project_id):
        try:
            project_ids_queryset = ProjectsAssigned.objects.filter(project=project_id)
            freelancer_id_list = []
            for i in project_ids_queryset:
                freelancer_id_list.append(i.freelancer)
            applied_queryset = ApplyProject.objects.filter(project=project_id,freelancer__in=freelancer_id_list).select_related('freelancer')
            result = []
            for applied in applied_queryset:
                result.append({
                    "details":ApplyedProjectAndFreelancerSerializer(applied).data
                })

            return Response({"serialized_data":result}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"errors":str(e)},status=status.HTTP_400_BAD_REQUEST)
class ProjectsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

#Get all projects
class GetAllProject(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        project_queryset = Projects.objects.all().order_by('-created_at')
        paginator = ProjectsPagination()
        paginated_queryset = paginator.paginate_queryset(project_queryset, request, view=self)
        serializer_instance = ProjectCreationSerializer(paginated_queryset, many=True)
        result = paginator.get_paginated_response(serializer_instance.data)
        return Response({"serialized_data":result.data},status=status.HTTP_200_OK)
    
#Get assinged Projects 
class GetAssingedProject(APIView):

    def get(self,request):
        assinged_project = Projects.objects.filter(project_assigned_status=True).all().order_by('-created_at')
        paginator = ProjectsPagination()
        paginated_queryset = paginator.paginate_queryset(assinged_project, request, view=self)
        serializer_instance = ProjectCreationSerializer(paginated_queryset, many=True)
        result = paginator.get_paginated_response(serializer_instance.data)
        return Response({"serialized_data":result.data},status=status.HTTP_200_OK)
   

# GET applied  Freelancers details for any project_id
class AppliedFreelancersVeiw(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,project_id):
        # get freelancers detail for specific project
        try:
            freelancer_data = []
            applied_project_freelancers  = ApplyProject.objects.filter(project=project_id).select_related('freelancer')
            print(applied_project_freelancers,"applied project")
            for application in applied_project_freelancers:
                freelancer = application.freelancer
                freelancer_data.append({
                    'freelancer_id': freelancer.pk,
                    'details': ApplyedProjectAndFreelancerSerializer(application).data
                })
                
            return Response({"serialized_data": freelancer_data}, status=status.HTTP_200_OK)
        except Exception as e :
            print(e)
            return Response({"errors":f"{e}"},status=status.HTTP_400_BAD_REQUEST)
        

class SendInvitaionToFreelancerView(APIView):
    def post(self,request):
        email = request.data['email']
        project_id = request.data['project_id']
        try:
            if not email or not project_id:
               return Response({'errors':'email and project_id is required'},status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(email=email)
            project = Projects.objects.get(pk=project_id)
            baseUrl = 'https://freelance.gokapinnotech.com'
            project_link = baseUrl + "/agent/dashboard/apply/" + str(project_id)
            subject = 'Invitation'
            html_message = render_to_string('invitation_email.html', {
                'project': project,
                'project_link': project_link
            })
            # Create plain text version of the email
            body  = f"""
                Dear { user.firstname },
                You have been invited to join a new project on our platform. Here are the details:
                { project.title }
                Description: {project.description }
                Budget: ${ project.project_price }
                To view the project and accept the invitation, please visit the following link:
                { project_link }
                If you have any questions, please don't hesitate to contact us.
                Best regards,
                Gokap team
                This is an automated message, please do not reply directly to this email.
                            """
            send_from = "gokap@gokapinnotech.com"
            send_to = [user.email]
            send_mail(subject,body,send_from,send_to,html_message=html_message)
            return Response({"msg":"success"},status=status.HTTP_200_OK)
        except Exception as e: 
            return Response({"errors":str(e)},status=status.HTTP_400_BAD_REQUEST)
        

class UserPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserSearchView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        name = request.query_params.get('name')
        email = request.query_params.get('email')
        role = request.query_params.get('role')
        print(role)
        queryset = User.objects.filter(user_type=role)
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

class UserDeleteView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def delete(self, request, id):
        try:
            user = User.objects.get(pk=id)
            if Projects.objects.filter(client_id=user.id).exists():
                return Response({'errors': 'Cannot delete user with active projects.'}, status=status.HTTP_400_BAD_REQUEST)
            user.delete()
            return Response({'message': 'User deleted successfully.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'errors': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

class ProjectUnAssignView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serialized = serializer.ProjectUnAssignSerializer(data=request.data)
        if serialized.is_valid():
            project = serialized.validated_data.get('project')
            freelancer = serialized.validated_data.get('freelancer')
            assigned_project = ProjectsAssigned.objects.filter(project=project,freelancer=freelancer)
            assigned_project.delete()
            project.project_assigned_status = False
            project.save()
            return Response({'msg':"Project unassigned success"},status=status.HTTP_200_OK)
        return Response({"errors":serialized.errors},status=status.HTTP_400_BAD_REQUEST)