from rest_framework import serializers
from project.models import ProjectsAssigned
from django.shortcuts import get_object_or_404

class ProjectAssignSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProjectsAssigned
        fields = ['frelancer','project',]
        
    def validate(self, attrs):
        try:
            project = get_object_or_404(ProjectsAssigned,project_id= attrs.get('project'))
            if project is not None:
                attrs['assigned'] = True
            return attrs
        except:
            attrs['assigned'] = False
            raise serializers.ValidationError
      