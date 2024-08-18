from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from project.models import Projects, ProjectsAssigned
from project.serializer import ProjectCreationSerializer
from . import serializer
from rest_framework.views import APIView
from register.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

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
                # raise ValueError("Project is Already Assigned. ")
                return Response({"error": "The Project is already assigned. "})
            
            frelancer_id = serialized.validated_data['frelancer_id']         
            project_id = serialized.validated_data['project_id']  
            print("the project id is : " , project_id)     
            print("the project id is : " , project_id.id)    
            print(type(project_id)) 
            obj = ProjectsAssigned.objects.create(frelancer_id=frelancer_id, project_id=project_id)
            project_data = serialized.ProjectAssignSerializer(obj)
            if obj is None:
                raise ValueError("Error Assigning Project")
            else:
                project = Projects.objects.get(id=project_id.id)
                project.project_assigned_status = True
                project.save()
                return Response({'msg': "Project Assigned", 'data':project_data.data})
        else:
            return Response({'error':serialized.errors})
        
    # To Unassign a Project 
    def delete(self, request):
        
        serialized = serializer.ProjectAssignSerializer(data=request.data)
        if serialized.is_valid():
            print("the delete serialiser is ", serialized.data)
            project_id = serialized.data['project_id']
            print(project_id, "this is project id ")
            if ProjectsAssigned.objects.get(project_id=project_id).exists():
            
                ProjectsAssigned.objects.get(project_id=project_id).delete()
                return JsonResponse({'msg':"UnAssigned"}, status=201)
            else:
                return JsonResponse({'msg':"Already  deleted"}, status=400)
        else:
            return JsonResponse({"errors":  serialized.errors, 'msg':'project doesnt existes.'}, status=400)
 
# get all the project assigned to a frelancer using the frelancer id
class GetAssignedProjectUsingFrelancerID(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(sef,request, frelancer_id):
        project_ids_queryset = ProjectsAssigned.objects.filter(frelancer_id=frelancer_id)
        print(project_ids_queryset.values())
        project_id_list = []
        for i in project_ids_queryset:
            project_id_list.append(i.project_id_id)
        print("the list of ids of assigned project is : ", project_id_list)
        project_queryset = Projects.objects.filter(id__in=project_id_list)
        serialized = ProjectCreationSerializer(project_queryset, many=True)
        return Response({"data":serialized.data}, status=status.HTTP_201_CREATED)
