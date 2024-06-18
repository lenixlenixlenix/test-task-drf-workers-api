from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

from django.contrib.auth import get_user_model

# Register your models here.

class CustomUserAdmin(UserAdmin):
    

    list_display = (
        'username', 'email', 'is_staff',
    )
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Additional info', {
            'fields': ('phone', 'is_client', 'is_employee')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        
    )
admin.site.register(CustomUser, CustomUserAdmin)


