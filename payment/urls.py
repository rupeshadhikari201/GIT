from django.urls import path
from payment.views import PaymentStatusView, create_payment

urlpatterns = [
    path('status/', PaymentStatusView.as_view(), name='project_status'),
    path('create-payment-intent/', create_payment, name='create_payment'),
]
