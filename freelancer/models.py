from django.db import models
from register.models import User
from django.contrib.postgres.fields import ArrayField

# Freelancer Model
class Freelancer(models.Model):
    WHERE_DID_YOU_HEARD = (
        ('I' , 'Instagram'),
        ('Fa' , 'Facebook'),
        ('F','Friends'),
        ('T' , 'Twitter'),
        ('TM','Team Member'),
        ('G' , 'Google'),
        ('O' , 'Others'),
        ('Y','Youtube')    
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profession = models.CharField(max_length=255)
    skills = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    languages = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    reason_to_join = models.TextField()
    where_did_you_heard = models.CharField(max_length=10, choices=WHERE_DID_YOU_HEARD)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    bio = models.TextField(blank=False,null=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)
