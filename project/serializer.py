from rest_framework import serializers
from project.models import ProjectFile, Projects, ProjectStatus

class ProjectCreationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Projects
        fields = '__all__'

class GetUnassingedProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Projects
        fields= '__all__'
        
# Project Status Serializer
class ProjectStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProjectStatus
        fields= '__all__'
        
# Project Profile File Serializer
class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = '__all__'
        