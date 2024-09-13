import os
from django.http import JsonResponse
from rest_framework.response import Response
from freelancer.serializer import  ApplyedProjectAndFreelancerSerializer
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
# Create your views here.
class ProjectAssignView(APIView):
    
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    # To Assign a Project
    def post(self, request):
        serialized = serializer.ProjectAssignSerializer(data=request.data)
        if serialized.is_valid():
            
            assigned = serialized.validated_data['assigned']
            
            if assigned:
                # raise ValueError("Project is Already Assigned.")
                return Response({"errors": "The Project is already assigned"},status=status.HTTP_400_BAD_REQUEST)
            frelancer_id = serialized.validated_data['frelancer_id']         
            project_id = serialized.validated_data['project_id']   
            obj = ProjectsAssigned.objects.create(frelancer_id=frelancer_id, project_id=project_id)
            project_data = serializer.ProjectAssignSerializer(obj)
            if obj is None:
                raise ValueError("Error Assigning Project")
            else:
                project = Projects.objects.get(id=project_id.id)
                project.project_assigned_status = True
                project.save()
                return Response({'msg': "Project Assigned", 'serialized_data':project_data.data},status=status.HTTP_200_OK)
        else:
            return Response(serialized.errors,status=status.HTTP_400_BAD_REQUEST)
        
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
    
    def get(self,request, frelancer_id):
        try:
            project_ids_queryset = ProjectsAssigned.objects.filter(frelancer=frelancer_id)
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
                freelancer_id_list.append(i.frelancer)
            applied_queryset = ApplyProject.objects.filter(project=project_id,frelancer__in=freelancer_id_list).select_related('frelancer')
            result = []
            for applied in applied_queryset:
                result.append({
                    "details":ApplyedProjectAndFreelancerSerializer(applied).data
                })

            return Response({"serialized_data":result}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"errors":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
#Get all projects
class GetAllProject(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        project_queryset = Projects.objects.all()
        serialized = ProjectCreationSerializer(project_queryset,many=True)
        return Response({'serialized_data':serialized.data},status=status.HTTP_200_OK)
    
#Get assinged Projects 
class GetAssingedProject(APIView):

    def get(self,request):
        assinged_project = Projects.objects.filter(project_assigned_status=True).all()
        serialized = ProjectCreationSerializer(assinged_project,many=True)
        return Response({'serialized_data':serialized.data},status=status.HTTP_200_OK)
# GET applied  Freelancers details for any project_id
class AppliedFreelancersVeiw(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,project_id):
        # get freelancers detail for specific project
        try:
            freelancer_data = []
            applied_project_freelancers  = ApplyProject.objects.filter(project=project_id).select_related('frelancer')
            print(applied_project_freelancers,"applied project")
            for application in applied_project_freelancers:
                freelancer = application.frelancer
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