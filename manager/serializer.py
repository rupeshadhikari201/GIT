from rest_framework import serializers
from project.models import ProjectsAssigned
from django.shortcuts import get_object_or_404

from register.models import User

class ProjectAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsAssigned
        fields = ['freelancer','project',]
        
    def validate(self, attrs):
        project = attrs.get('project')
        exits = ProjectsAssigned.objects.filter(project=project).exists()
        if exits:
            raise serializers.ValidationError("Project is already assigned ")
        return attrs

        


class SendInvitationToFreelancerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    
    class Meta:
        model = User
        fields = ['email']
      