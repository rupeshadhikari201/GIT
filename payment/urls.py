from django.urls import path
from payment.views import PaymentStatusView

urlpatterns = [
    path('status/', PaymentStatusView.as_view(), name='project_status'),
]
