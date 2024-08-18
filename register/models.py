from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from jsonschema import ValidationError


class UserManager(BaseUserManager):
    
    def create_user(self, firstname, lastname, email, password=None, cnfpassword=None,user_type=None):
        """
        Creates and saves a User with the given firstname, lastname, email, password
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            firstname = firstname,
            lastname = lastname,
            email=self.normalize_email(email), 
            password = password, 
            user_type=user_type    
        )

        user.set_password(password)
        user.save(using=self.db)
        Address.objects.create(user=user) # Create an address for the user
        return user

    def create_superuser(self, firstname, lastname, email, password=None, ):
        """
        Creates and saves a superuser with the given firstname, lastname, email,password=None, cnfpassword=None
        """
        user = self.create_user(
            firstname = firstname,
            lastname = lastname,
            email = email, 
            password = password,
            user_type='superuser'      
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom Model
class User(AbstractBaseUser):
    
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )   
    password = models.CharField(max_length=255)
    
    user_type = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False, verbose_name='email verified')
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now=True) 
    

    objects = UserManager()

    USERNAME_FIELD = "email"    #takes email to login user
    REQUIRED_FIELDS = ["firstname", "lastname", "password",]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


    


# Notification Model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user.username} - {self.message}'
    

    
class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.TextField()
    state = models.TextField()
    city = models.TextField()
    zip_code = models.TextField()

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname} - {self.city}, {self.state}, {self.country}, {self.zip_code}"
