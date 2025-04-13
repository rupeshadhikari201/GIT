from django.db import models

# Create your models here.
class Feedback(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
