from django.db import models
from payment.models import PaymentStatus
from client.models import Client
from django.contrib.postgres.fields import ArrayField
from freelancer.models import Freelancer
from rest_framework.validators import ValidationError

# Create your models here.
class ProjectStatus(models.Model):
      
    PROJECT_STATUS = (
        ('C', 'Completed'),
        ('O', 'Onging'),
        ('P', 'Paused'),
        ('UN', 'UnAssigned')
    )  
    project_status = models.CharField(choices=PROJECT_STATUS, max_length=20)
    
    def __str__(self):
        return self.project_status
    
class Projects(models.Model):
    
    # get the defualt payment status
    def get_default_payment_status():
        return PaymentStatus.objects.get(payment_status='UN').pk
    
    # get the defualt project status
    def get_default_project_status():
        return ProjectStatus.objects.get(project_status='UN').pk

    CATEGORIES = (
        ('R',  'Research'),
        ('D', 'Design'),
        ('Dev', 'Development'),
        
    )
    project_category = models.CharField(choices=CATEGORIES, max_length=20)
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    project_price = models.IntegerField()
    project_deadline = models.DateTimeField()
    skills_required = ArrayField(models.CharField(max_length=100), default=list)
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE, default=get_default_payment_status)
    project_status = models.ForeignKey(ProjectStatus, on_delete=models.CASCADE, default=get_default_project_status)
    project_assigned_status = models.BooleanField(default=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects_created')
    applied_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return str(self.id)
    
class ProjectsAssigned(models.Model):
    
    frelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    revoke = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if ProjectsAssigned.objects.filter(project_id=self.project_id).exists():
            raise ValidationError(f"Project {self.project_id} is already assigned to a freelancer")
        else:
            super().save(*args, **kwargs)
    
# Apply Project
class ApplyProject(models.Model):
    class Meta:
        unique_together = ('project','frelancer')
    STATUS_CHOICES = [
        ('PA', 'Pending Approval'),
        ('AC', 'Accepted'),
        ('RE', 'Rejected'),
    ]
    
    frelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    proposal = models.TextField(blank=False)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PA')
    
    def __str__(self):
        return f'Project id : {self.project_id}'
      
# Model to store project screenshot
class ProjectFile(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    file = models.FileField(upload_to='project_files/')             #Access the uploaded image via the URL: https://your-app.onrender.com/media/project_files/your_image.jpg.
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name