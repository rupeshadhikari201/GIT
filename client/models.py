from django.db import models
from register.models import User

# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)

    class Meta:
        swappable : "User"
    def __str__(self):
        # return self.user.username
        return self.user.email