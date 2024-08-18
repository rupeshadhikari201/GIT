from django.db import models
from django.apps import apps

# from project.models import Projects
# from project import models as project_model

class PaymentStatus(models.Model):
    PAYMENT_STATUS = (
        ('P', 'Paid'),
        ('UN', 'Unpaid'),
        ('PP', 'Partially Paid')
    )
    payment_status = models.CharField(choices = PAYMENT_STATUS, max_length=20)
    
    def __str__(self):
        return self.payment_status
    
# Create your models here.
class Payment(models.Model):
    # project_model = apps.get_model('project','Projects')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey('project.Projects', on_delete=models.CASCADE, related_name='payments')

    
    def __str__(self):
        return f"${self.amount} - {self.payment_status}"