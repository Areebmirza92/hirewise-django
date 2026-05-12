"""
accounts/admin.py — Register User model with Django admin
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'get_full_name', 'role', 'domain', 'is_active', 'date_joined')
    list_filter = ('role', 'domain', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {
            'fields': (
                'role', 'phone', 'address', 'domain',
                'position_applied_for', 'experience',
                'skills', 'certifications', 'resume',
            )
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Profile', {
            'fields': ('role', 'email', 'domain'),
        }),
    )
