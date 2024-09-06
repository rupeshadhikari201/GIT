from rest_framework import serializers
from project.models import Projects
from .models import Client
from register.models import User

# This class defines a serializer for the Client Model. 
# It helps in Converting Client's Model instance into JSON format and vice-versa.
# ModelSerializer is a DRF class that creates a serializer class based on fields of Django Model
class ClientCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['user']
    
    # A Custom Function to validate fields of Client Model
    def validate(self, attrs):
        if not User.objects.filter(id=attrs).exists():
           raise serializers.ValidationError("User does not exist")
        return attrs

    # This overrides the default create function to customize how client instance is created when using the serializer
    # It's invoked when the serializer's is_valid() method returns True
    def create(self, validated_data):
        user_id = validated_data.pop('user')
        user = User.objects.get(id=user_id)
        # The **validated_data syntax unpacks the dictionary, allowing additional fields to be passed as keyword arguments.'
        # validated_data :- It contains only the fields defined in the serializer.
        print("The unpacked validated_data is ; ", **validated_data)
        client = Client.objects.create(user=user, **validated_data)
        return client

class GetClientProjectsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Projects
        fields = "__all__" 
         
