"""
jobs/admin.py — Register Job and Application models
"""

from django.contrib import admin
from .models import Job, Application


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'domain', 'recruiter', 'created_at')
    list_filter = ('domain',)
    search_fields = ('title', 'description')
    ordering = ('-created_at',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'job', 'status', 'applied_at')
    list_filter = ('status',)
    search_fields = ('applicant__email', 'job__title')
    ordering = ('-applied_at',)
    actions = ['accept_selected', 'reject_selected']

    def accept_selected(self, request, queryset):
        queryset.update(status='accepted')
    accept_selected.short_description = "Accept selected applications"

    def reject_selected(self, request, queryset):
        queryset.update(status='rejected')
    reject_selected.short_description = "Reject selected applications"
