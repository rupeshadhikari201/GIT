from django.shortcuts import render
from django.db.models import Q
from register.models import User
from register.renderers import UserRenderer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Freelancer
from .serializer import FreelancerDetailsSerializer,FreelancerCreationSerializer
from rest_framework.response import Response
from rest_framework import status
from project.models import Projects, ApplyProject
from freelancer import serializer

# API to Create Freelancer
class FreelancerCreationView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        # The data that we are getting from post request doesn't contains 'user', so we need to append 'user' because, Freelancer Model has 'user' attribute
        data = request.data.copy()
        user_id = request.user.id
        data['user'] = user_id
        print("the final data is : ", data)
        
        # This line creates an instance of the FreelancerSerializer class. 
        # It takes the request.data as the data to be serialized.
        serialized = FreelancerCreationSerializer(data=data)
        
        # This line checks whether the data provided to the serializer is valid according to the serializer's validation rules. The is_valid() method is a DRF method that triggers the validation process.
        if serialized.is_valid():
            # If the data is valid, this line saves the data to the database.
            serialized.save()
            return Response({"msg": "Freelancer Created", "serialized_data": serialized.data}, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # get all the frelancers
    def get(self, request):
        # Get the queryset 
        freelancers = Freelancer.objects.all()
        # The many parameter is a boolean flag used to indicate whether the serializer should be used to serialize a single instance (many=False) or multiple instances (many=True)
        serialized = FreelancerCreationSerializer(freelancers, many=True)
        
        return Response({'serialized_data': serialized.data})
        
# Get Freelancer (by Authentication)
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

# Update Freelancer View
class UpdateFreelancerView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        user = request.user
        data = request.data
        data['user'] = user.id
        freelancer = Freelancer.objects.get(user=user.id)
        serialized = FreelancerCreationSerializer(freelancer,data=data,partial=True)
        if serialized.is_valid():
            serialized.save()
            return Response({'msg':"success", 'serialized_data': serialized.data}, status=status.HTTP_200_OK)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)  
        
    def patch(self, request):
        pass
       
# Apply Projects View
class ApplyProjectView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        print("id", request.user.id)
        data = request.data
        data['frelancer_id'] = request.user.id
        serialized = serializer.ApplyProjectSerializer(data= data)
        print("data is",data)
        project = Projects.objects.get(pk=data['project_id'])
        if serialized.is_valid():
            serialized.save()
            project.applied_count += 1
            project.save()
            return Response({"msg": "Project Applied Sucess"}, status=status.HTTP_200_OK)
        return Response({"error": serialized.errors}, status=status.HTTP_404_NOT_FOUND)

# GET applied Freelancers details For any project_id
class AppliedFreelancersView(APIView):
    
    def get(self,request,project_id):
        # get freelancers detail for specific project
        try:
           
            freelancer_data = []
            applied_project_freelancer  = ApplyProject.objects.filter(project_id=project_id).select_related('frelancer_id')
            for application in applied_project_freelancer:
                freelancer = application.frelancer_id
                freelancer_data.append({
                    'freelancer_id': freelancer.pk,
                    'details': serializer.ApplyProjectSerializer(application).data
                })
                
            return Response({"freelancers": freelancer_data}, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error":f"{e}"},status=status.HTTP_400_BAD_REQUEST)

# The API to get all the applied projects of a particular freelancer based on their token
class GetAppliedProject(APIView):
    
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # 1. get the user 
        user = request.user
        
        try:
            freelancer = Freelancer.objects.get(user=user)
            applied_projects = ApplyProject.objects.filter(frelancer_id=freelancer).select_related('project').all()
            try:
                serialized = serializer.ApplyProjectAndProjectSerializer(applied_projects, many=True)
                return Response({'serialized_data': serialized.data}, status=status.HTTP_200_OK)
            except Exception as e: 
                return Response({'errors' : str(e)},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'errors': str(e),}, status=status.HTTP_404_NOT_FOUND)
#Get appliedProjectById
class GetAppliedProjectById(APIView):
    
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def get(self, request,applied_id):
        # 1. get the user 
        user = request.user
        
        try:
            freelancer = Freelancer.objects.get(user=user)
            applied_projects = ApplyProject.objects.filter(pk=applied_id,frelancer_id=freelancer).select_related('project').all()
            print(applied_projects.values_list(),"applied projects")
            try:
                serialized = serializer.ApplyProjectAndProjectSerializer(applied_projects,many=True)
                return Response({'serialized_data': serialized.data}, status=status.HTTP_200_OK)
            except Exception as e: 
                return Response({'errors' : str(e)},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'errors': str(e),}, status=status.HTTP_404_NOT_FOUND)
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

# get all the details of all the frelancers
class GetDetailsOfFrelancers(APIView):
    
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated] 
    
    def get(self,request):
        frelancers_queryset = User.objects.filter(user_type="freelancer")
        serialized = serializer.GetDetailsOfFrelancersSerializer(frelancers_queryset, many=True)
        return Response({"serialized_data": serialized.data}, status=status.HTTP_200_OK)