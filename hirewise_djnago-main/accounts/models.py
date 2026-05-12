"""
accounts/models.py — Custom User Model for Hirewise
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('applicant', 'Applicant'),
        ('recruiter', 'Recruiter'),
    ]

    # Override email to be unique and required
    email = models.EmailField(unique=True)

    # Role field
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='applicant')

    # ── Shared fields ──────────────────────────────────────────
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    domain = models.CharField(max_length=100, blank=True, null=True,
                              help_text="Industry domain e.g. Technology, Finance")

    # ── Applicant-specific fields ──────────────────────────────
    position_applied_for = models.CharField(max_length=200, blank=True, null=True,
                                            help_text="Desired job position")
    experience = models.TextField(blank=True, null=True,
                                  help_text="Work experience summary")
    skills = models.TextField(blank=True, null=True,
                              help_text="Skills (comma-separated)")
    certifications = models.TextField(blank=True, null=True,
                                      help_text="Certifications and qualifications")
    resume = models.FileField(upload_to='resumes/', blank=True, null=True,
                              help_text="Upload your CV/resume (PDF or DOCX)")

    # Use email as the login identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    @property
    def full_name(self):
        return self.get_full_name() or self.username

    @property
    def is_applicant(self):
        return self.role == 'applicant'

    @property
    def is_recruiter(self):
        return self.role == 'recruiter'
