"""
jobs/models.py — Job and Application models for Hirewise
"""

from django.db import models
from django.conf import settings


class Job(models.Model):
    DOMAIN_CHOICES = [
        ('Technology', 'Technology'),
        ('Finance', 'Finance'),
        ('Media', 'Media'),
        ('E-Commerce', 'E-Commerce'),
        ('Healthcare', 'Healthcare'),
        ('Education', 'Education'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    domain = models.CharField(max_length=100, choices=DOMAIN_CHOICES)
    recruiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posted_jobs',
        limit_choices_to={'role': 'recruiter'}
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'jobs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.domain}"


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications',
        limit_choices_to={'role': 'applicant'}
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'applications'
        unique_together = ('job', 'applicant')   # prevent duplicate applications
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.applicant.full_name} → {self.job.title} [{self.status}]"
