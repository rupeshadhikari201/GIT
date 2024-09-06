import ast
from register.models import User
from .models import Freelancer
from project.models import ApplyProject
from rest_framework import serializers
from common.serializer import UserRegistrationSerializer
from project.serializer import ProjectCreationSerializer

class FreelancerCreationSerializer(serializers.ModelSerializer):
    
    skills = serializers.ListField(child=serializers.CharField())
    languages = serializers.ListField(child=serializers.CharField())
    
    class Meta:
        model = Freelancer
        fields = ['user', 'profession', 'skills','languages', 'reason_to_join','where_did_you_heard', 'resume','bio','updated_at']
    
    '''
    The "to_internal_value" method is part of Django REST framework's serializer validation process. It is responsible for converting the incoming primitive data types (typically JSON) into native Python data types and validating them. This method is usually overridden to perform custom deserialization and validation.
    '''
    def to_internal_value(self, data):
        if 'skills' in data and isinstance(data['skills'], str):
            data['skills'] = data['skills'].strip('][').split(', ')
            
        if 'languages' in data and isinstance(data['languages'], str):
            data['languages'] = data['languages'].strip('][').split(', ')
        
        # After converting the skills and languages fields to lists, the method calls super().to_internal_value(data) to leverage the default behavior provided by ModelSerializer. 
        return super().to_internal_value(data)
    
    '''
    The validate method in a Django REST framework serializer is used to provide custom validation logic. The commented-out validate method you provided attempts to process the skills attribute, but it has some issues.
    '''
    def validate(self, attrs):
        # retrive the skills attribute from the attrs dictionary, which contains all the validated data
        skills = attrs.get('skills')
        
        # check if the skills is an instance of string
        if isinstance(skills, str):
            
            # The ast.literal_eval function safely evaluates a string containing a Python literal or container display (like a list, dictionary, or string) and converts it into an actual Python object. This line assumes that skils is a string representation of a list and attempts to convert it into a Python list.
            try:
                skills_list = ast.literal_eval(skills)
                
                if not isinstance(skills_list, list):
                    raise ValueError
            
            except (ValueError,SyntaxError):
                raise serializers.ValidationError({'skills': 'Invalid format for skills. Must be a list or a string representation of a list.'})
            
            attrs['skills'] = skills_list
            
        return attrs
    
class FreelancerDetailsSerializer(serializers.ModelSerializer):
    
    user= UserRegistrationSerializer(read_only=True)
    
    class Meta:
        model = Freelancer
        fields = '__all__'
        
class ApplyProjectSerializer(serializers.ModelSerializer):
    frelancer_id = FreelancerDetailsSerializer(read_only=True)
    class Meta:
        model = ApplyProject
        fields = '__all__'
        
class ApplyProjectAndProjectSerializer(serializers.ModelSerializer):
    project = ProjectCreationSerializer(read_only=True)
    class Meta:
        model = ApplyProject
        fields = '__all__'
  
# get all Frelancers Serializer 
class GetDetailsOfFrelancersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']