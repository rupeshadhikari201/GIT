# Payment Status Serializer
from payment.models import PaymentStatus
from rest_framework import serializers

class PaymentStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PaymentStatus
        fields= '__all__'