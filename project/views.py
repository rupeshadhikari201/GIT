from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from register.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from project.models import ProjectFile, ProjectStatus, Projects
from project import serializer
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response


# API for ProjectCreation Serializer
class ProjectCreationView(APIView):
    
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        data = request.data
        data['client'] = request.user.id
        print(data)
        serialized = serializer.ProjectCreationSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"msg":"Project Created!", "details": serialized.data}, status=status.HTTP_201_CREATED)
        return Response({"errors": serialized.errors}, status=status.HTTP_400_BAD_REQUEST)
   
# API for ProjectUpdation Serializer 
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
        
        serialized = serializer.ProjectCreationSerializer(project, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response({"msg":"Project Updated!", "details": serialized.data}, status=status.HTTP_201_CREATED)
        return Response({ "errors": serialized.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request, project_id, *args, **kwargs):
        project = self.get_object(project_id)
        if project is None:
            return Response({'msg': "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializered = serializer.ProjectCreationSerializer(project, data=request.data, partial=True)
        if serializered.is_valid():
            serializered.save()
            return Response({"msg": "Project Updated!", "details": serializered.data}, status=status.HTTP_200_OK)
        return Response({"errors": serializered.errors}, status=status.HTTP_400_BAD_REQUEST)

# API to FilterProject Serializer
class PriceFilterView(APIView): 
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, price_start, price_end, n_applicant): 
        
        if(n_applicant < 0 and price_end > 0):
             queryset = Projects.objects.filter(project_price__range=(price_start,price_end))
             serialized = serializer.ProjectCreationSerializer(queryset, many=True)
             return Response({'serialized_data': serialized.data}, status=status.HTTP_201_CREATED)
        if(n_applicant >=0 and price_end > 0):
             queryset = Projects.objects.filter(applied_count__range=(0,n_applicant)  ,project_price__range=(price_start,price_end))
             serialized = serializer.ProjectCreationSerializer(queryset, many=True)
             return Response({'serialized_data': serialized.data}, status=status.HTTP_201_CREATED)
        if(price_end <= 0 and n_applicant >=0):
             queryset = Projects.objects.filter(applied_count__range=(0,n_applicant))
             serialized = serializer.ProjectCreationSerializer(queryset, many=True)
             return Response({'serialized_data': serialized.data}, status=status.HTTP_201_CREATED)
        if(price_end == 0 and n_applicant < 0):
            return Response({"error":"Invalid filter"},status=status.HTTP_400_BAD_REQUEST)  

# API to SearchProject Serializer           
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

        serialized = serializer.ProjectCreationSerializer(queryset, many=True)
        return Response({'serialized_data': serialized.data}, status=status.HTTP_200_OK)
    
# API to GetUnassignedProject 
class GetUnassingedProjects(APIView):
    
    renderer_classes = [UserRenderer]
    
    def get(self, request):
        # Fetch all projects that are not assigned
        unassigned_projects = Projects.objects.filter(project_assigned_status=False).order_by('-created_at')
        serializered = serializer.GetUnassingedProjectSerializer(unassigned_projects, many=True)
        return Response({'data': serializered.data, 'msg': "Unassigned Projects Retrieved Successfully"}, status=status.HTTP_200_OK)

# Delete Unassigned Project Project
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
    
# Get the Projects Details by Project Id
class GetProjectDetailsByIdView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes =  [ IsAuthenticated]
    
    def get(self, request,project_id):
        projects = get_object_or_404(Projects,pk=project_id)
        serializered = serializer.ProjectCreationSerializer(projects)
        
        return Response({"serialized_data":serializered.data})
    
# API Database for holding project screenshots, doc and pdf files
class ProjectFileView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        project_files = ProjectFile.objects.filter(project_id=project_id)
        serializered = serializer.ProjectFileSerializer(project_files, many=True)
        return Response({'data': serializered.data}, status=status.HTTP_200_OK)

    def post(self, request, project_id):
        data = request.data
        data['project'] = project_id
        serializered = serializer.ProjectFileSerializer(data=data)
        if serializered.is_valid():
            serializered.save()
            return Response({'msg': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializered.errors}, status=status.HTTP_400_BAD_REQUEST)
    
# API's to populate ProjectStatus
class ProjectStatusView(generics.ListCreateAPIView):
    
    queryset = ProjectStatus.objects.all()
    serializer_class = serializer.ProjectStatusSerializer