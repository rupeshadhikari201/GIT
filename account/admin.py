from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class UserAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id", "firstname", "lastname", "email","is_admin", "created_at","updated_at"]
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


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)