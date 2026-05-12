"""
jobs/forms.py — Job posting form for Hirewise
"""

from django import forms
from .models import Job


class PostJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'domain', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'id': 'job-title',
                'placeholder': 'e.g. Senior Software Engineer'
            }),
            'domain': forms.Select(attrs={
                'id': 'job-domain'
            }),
            'description': forms.Textarea(attrs={
                'id': 'job-description',
                'rows': 5,
                'placeholder': 'Describe the role, responsibilities, and requirements…'
            }),
        }
