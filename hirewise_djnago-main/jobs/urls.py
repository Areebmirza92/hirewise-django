"""
jobs/urls.py — URL patterns for jobs and applications
"""

from django.urls import path
from . import views

urlpatterns = [
    # ── Applicant ───────────────────────────────────────────
    path('jobs/',                    views.browse_jobs,         name='browse_jobs'),
    path('jobs/<int:job_id>/apply/', views.apply_job,           name='apply_job'),
    path('my-applications/',         views.my_applications,     name='my_applications'),

    # ── Recruiter ───────────────────────────────────────────
    path('recruiter/post-job/',                 views.post_job,            name='post_job'),
    path('recruiter/applicants/',               views.manage_applications, name='manage_applications'),
    path('recruiter/applications/<int:app_id>/status/', views.update_status, name='update_status'),
    path('recruiter/resume/<int:user_id>/',     views.download_resume,     name='download_resume'),
]
