
from django.contrib import admin
from freelancer.models import Freelancer
from payment.models import Payment, PaymentStatus
from project.models import ProjectStatus, Projects, ProjectsAssigned
from register.models import Address,User
from client.models import Client
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class UserAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model. These override the definitions on the base UserAdmin, that reference specific fields on auth.User.
   
    list_display = ["id", "firstname", "lastname", "email","is_admin","user_type","created_at","updated_at"]
    list_filter = ["is_admin", "id","created_at","email", "lastname"]
    fieldsets = [
        ("Credential Informations", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["firstname", "lastname"]}),
        ("Permissions", {"fields": ["is_admin"]}),
        ("Timestamps", {'fields': ["created_at", "updated_at"]}),
    ]
    readonly_fields = ["created_at", "updated_at"]
    
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["firstname","lastname","email", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email", "lastname"]
    ordering = ["email"]
    filter_horizontal = []
    

# Now register the new UserAdmin..
admin.site.register(User, UserAdmin)
admin.site.register(Freelancer)
admin.site.register(Payment)
admin.site.register(PaymentStatus)
admin.site.register(ProjectStatus)
admin.site.register(Client)
admin.site.register(Projects)
admin.site.register(Address)
admin.site.register(ProjectsAssigned)
