
from django.contrib import admin, messages
from django.forms import ModelForm
from django.core.exceptions import ValidationError
import requests
from freelancer.models import Freelancer
from payment.models import Payment, PaymentStatus
from project.models import ProjectStatus, Projects, ProjectsAssigned
from register.models import Address,User
from client.models import Client
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# # custom project assign form 
# class ProjectAssignForm(ModelForm):
#     class Meta:
#         model = ProjectsAssigned
#         fields = '__all__'
    
#     def clean(self):
#         cleaned_data = super().clean()
#         print("Cleaned Project Assigned Data is : ", cleaned_data)
#         project_id = cleaned_data.get('project_id')
#         if ProjectAssignForm.objects.filter(project_id=project_id).exists():
#             raise ValidationError(f"{project_id :} is  already assigned to a freelancer")
#         return cleaned_data

# class ProjectAssignedInline(admin.TabularInline):
#     model = ProjectsAssigned
#     # The extra attribute in the context of Django's TabularInline or StackedInline classes determines the number of empty forms that will be displayed in the inline formset when adding or editing a related object in the admin interface.
#     extra = 5

# # class ProjectsAdmin(admin.ModelAdmin):
#     # inlines = [ProjectAssignedInline]
    
# # class FreelancerAdmin(admin.ModelAdmin):
#     # inlines = [ProjectAssignedInline]

    
# # 2. Create a Custom Admin Action to Use the API
# # You can create a custom admin action that calls your API to assign projects. This way, even when using the admin interface, the assignment logic is handled by your API.
# def assign_project_via_api(modeladmin, request, queryset):
#     for project in queryset:
#         # Example: Assign the first available freelancer
#         freelancer = Freelancer.objects.first()
#         if freelancer:
#             response = requests.post(
#                 'http://localhost:8000/api/user/assign-projects/',
#                 json={
#                     'project_id': project.id,
#                     'frelancer_id': freelancer.id
#                 },
#                 headers={
#                     'Authorization': f'Bearer {request.user.auth_token.key}'
#                 }
#             )
#             if response.status_code == 200:
#                 messages.success(request, f' This... Project {project.title} assigned to {freelancer.user.email}')
#             else:
#                 messages.error(request, f'Failed to assign project {project.title}: {response.json().get("error", "Unknown error")}')
#         else:
#             messages.error(request, 'No available freelancer to assign')

# assign_project_via_api.short_description = "Assign selected projects to a freelancer via API"

# class ProjectsAdmin(admin.ModelAdmin):
    # actions = [assign_project_via_api]           
    

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
# admin.site.register(Projects)
admin.site.register(Projects)
admin.site.register(Address)
admin.site.register(ProjectsAssigned)
# admin.site.register(ProjectAssignForm)