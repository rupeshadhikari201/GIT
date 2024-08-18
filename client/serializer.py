from rest_framework import serializers
from project.models import Projects
from .models import Client
from register.models import User


class ClientCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['user']

    def validate_user(self, value):
        print("the value is : ", value)
        return value

    def create(self, validated_data):
        user_id = validated_data.pop('user')
        user = User.objects.get(id=user_id)
        client = Client.objects.create(user=user, **validated_data)
        return client

class GetClientProjectsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Projects
        fields = "__all__" 
         
