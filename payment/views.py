import json
import stripe
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from payment.serializer import PaymentStatusSerializer
from payment.models import PaymentStatus
import os

# Set the secret key
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
print(stripe.api_key)

@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = int(data['amount'])  # Amount should be in cents, e.g., $10 = 1000

            # Create a PaymentIntent with the order amount and currency
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
            )

            return JsonResponse({
                'clientSecret': payment_intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)







# API's to populate ProjectStatusa
class PaymentStatusView(generics.ListCreateAPIView):
    
    queryset = PaymentStatus.objects.all()
    serializer_class = PaymentStatusSerializer