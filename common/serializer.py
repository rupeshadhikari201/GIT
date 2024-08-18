from rest_framework import serializers
from register.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    cnfpassword = serializers.CharField(style={'input_type' : 'password'},write_only=True)
    class Meta:
        model = User
        fields = ['firstname','lastname','email','password', 'cnfpassword',"user_type", "id"]
        extra_kwargs = {
            'password' : {'write_only': True}
        }
        
    # Validate Password and cnfpassword
    def validate(self, attrs):
        password = attrs.get('password')
        cnfpassword = attrs.get('cnfpassword')
        if password != cnfpassword:
            raise serializers.ValidationError("Password and Confirm password must be same!")
        return attrs
    
    # Create Method
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)