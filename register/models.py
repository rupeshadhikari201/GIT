from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

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
    
    
class Freelancer(models.Model):
    WHERE_DID_YOU_HEARD = (
        ('I' , 'Instagram'),
        ('F' , 'Facebook'),
        ('T' , 'Twitter'),
        ('G' , 'Google'),
        ('O' , 'Others')    
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profession = models.CharField(max_length=255)
    skills = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    languages = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    reason_to_join = models.TextField()
    where_did_you_heard = models.CharField(max_length=1, choices=WHERE_DID_YOU_HEARD)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    bio = models.TextField()

    def __str__(self):
        return str(self.user)
 

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    # Reverse relationship for projects uploaded by the client
    # projects_uploaded = models.ManyToManyField('Projects', related_name='uploaded_by_clients', blank=True, null=True)
    # Reverse relationship for payments made by the client
    # payments_paid = models.ManyToManyField('Payment', related_name='payments_paid_by_clients') 

    class Meta:
        swappable : "User"
    def __str__(self):
        return self.user.username

class ProjectStatus(models.Model):
      
    PROJECT_STATUS = (
        ('C', 'Completed'),
        ('O', 'Onging'),
        ('P', 'Paused'),
        ('UN', 'UnAssigned')
    )  
    project_status = models.CharField(choices=PROJECT_STATUS)
    
    def __str__(self):
        return self.project_status

class PaymentStatus(models.Model):
    PAYMENT_STATUS = (
        ('P', 'Paid'),
        ('UN', 'Unpaid'),
        ('PP', 'Partially Paid')
    )
    payment_status = models.CharField(choices = PAYMENT_STATUS)
    
    def __str__(self):
        return self.payment_status

class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey('Projects', on_delete=models.CASCADE, related_name='payments')
    # payment_date = 
    # transaction_status =
    
    def __str__(self):
        return f"${self.amount} - {self.payment_status}"
    
class Projects(models.Model):
    CATEGORIES = (
        ('R',  'Research'),
        ('D', 'Design'),
        ('Dev', 'Development'),
        
    )
    project_category = models.CharField(choices=CATEGORIES)
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    project_price = models.IntegerField()
    project_deadline = models.DateTimeField()
    skills_required = ArrayField(models.CharField(max_length=100), default=list)
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE, default=1)
    project_status = models.ForeignKey(ProjectStatus, on_delete=models.CASCADE, default=1)
    
    project_assigned_status = models.BooleanField(default=False)

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects_created')
    # freelancer = models.ForeignKey(Freelancer, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects_allocated')
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return self.title
    
class ProjectsAssigned(models.Model):
    
    frelancer_id = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    revoke = models.BooleanField(default=False)
    
