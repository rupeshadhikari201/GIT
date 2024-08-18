from rest_framework import generics
from payment.serializer import PaymentStatusSerializer
from payment.models import PaymentStatus

# Create your views here.


# API's to populate ProjectStatus
class PaymentStatusView(generics.ListCreateAPIView):
    
    queryset = PaymentStatus.objects.all()
    serializer_class = PaymentStatusSerializer