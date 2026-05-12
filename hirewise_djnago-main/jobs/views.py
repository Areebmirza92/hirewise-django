"""
jobs/views.py — Job browsing, applying, posting, and managing applications
"""

import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from django.db.models import Q
from .models import Job, Application
from .forms import PostJobForm
from accounts.models import User


# ── Decorator: require applicant role ────────────────────────
def applicant_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth')
        if request.user.role != 'applicant':
            return redirect('post_job')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# ── Decorator: require recruiter role ────────────────────────
def recruiter_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth')
        if request.user.role != 'recruiter':
            return redirect('browse_jobs')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# ════════════════════════════════════════════════════════════
#  APPLICANT VIEWS
# ════════════════════════════════════════════════════════════

@applicant_required
def browse_jobs(request):
    """
    Applicant: Browse all jobs with optional domain filter.
    Also determines which jobs the user has already applied to.
    """
    domain = request.GET.get('domain', 'All')
    jobs = Job.objects.select_related('recruiter').all()
    if domain and domain != 'All':
        jobs = jobs.filter(domain=domain)

    # Pre-fetch applied job IDs for this user
    applied_ids = set(
        Application.objects.filter(applicant=request.user)
        .values_list('job_id', flat=True)
    )

    return render(request, 'jobs/browse.html', {
        'jobs': jobs,
        'applied_ids': applied_ids,
        'selected_domain': domain,
        'domains': ['All', 'Technology', 'Finance', 'Media', 'E-Commerce', 'Healthcare', 'Education', 'Other'],
    })


@applicant_required
def apply_job(request, job_id):
    """
    Applicant: Apply for a specific job.
    Auto-attaches the applicant's resume from their profile.
    """
    if request.method != 'POST':
        return redirect('browse_jobs')

    job = get_object_or_404(Job, id=job_id)
    applicant = request.user

    # Prevent duplicate application
    if Application.objects.filter(job=job, applicant=applicant).exists():
        messages.warning(request, 'You have already applied for this position.')
        return redirect('browse_jobs')

    Application.objects.create(job=job, applicant=applicant, status='pending')
    messages.success(request, f'Successfully applied for "{job.title}"!')
    return redirect('browse_jobs')


@applicant_required
def my_applications(request):
    """
    Applicant: View all submitted applications with their status.
    """
    apps = (Application.objects
            .filter(applicant=request.user)
            .select_related('job', 'job__recruiter')
            .order_by('-applied_at'))

    return render(request, 'jobs/my_applications.html', {'applications': apps})


# ════════════════════════════════════════════════════════════
#  RECRUITER VIEWS
# ════════════════════════════════════════════════════════════

@recruiter_required
def post_job(request):
    """Recruiter: Post a new job vacancy."""
    if request.method == 'POST':
        form = PostJobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            messages.success(request, f'Job "{job.title}" posted successfully!')
            return redirect('post_job')
    else:
        form = PostJobForm()

    # Also list the recruiter's own jobs
    my_jobs = Job.objects.filter(recruiter=request.user).order_by('-created_at')
    return render(request, 'jobs/post_job.html', {'form': form, 'my_jobs': my_jobs})


@recruiter_required
def manage_applications(request):
    """
    Recruiter: See all applicants for jobs they posted.
    Grouped by job, with full profile + resume download link.
    """
    apps = (Application.objects
            .filter(job__recruiter=request.user)
            .select_related('job', 'applicant')
            .order_by('job__title', '-applied_at'))

    return render(request, 'jobs/manage_applications.html', {'applications': apps})


@recruiter_required
def update_status(request, app_id):
    """Recruiter: Accept or reject a specific application."""
    if request.method != 'POST':
        return redirect('manage_applications')

    app = get_object_or_404(Application, id=app_id, job__recruiter=request.user)
    new_status = request.POST.get('status')

    if new_status not in ['accepted', 'rejected']:
        messages.error(request, 'Invalid status.')
        return redirect('manage_applications')

    app.status = new_status
    app.save()

    action = 'accepted' if new_status == 'accepted' else 'rejected'
    messages.success(request, f'Application by {app.applicant.full_name} has been {action}.')
    return redirect('manage_applications')


@recruiter_required
def download_resume(request, user_id):
    """
    Recruiter: Download/view an applicant's resume file.
    Only accessible to recruiters who have a matching application.
    """
    applicant = get_object_or_404(User, id=user_id, role='applicant')

    # Security: only allow if recruiter has at least one application from this applicant
    has_access = Application.objects.filter(
        applicant=applicant,
        job__recruiter=request.user
    ).exists()

    if not has_access:
        raise Http404("Resume not found or access denied.")

    if not applicant.resume:
        messages.error(request, 'This applicant has not uploaded a resume.')
        return redirect('manage_applications')

    file_path = applicant.resume.path
    if not os.path.exists(file_path):
        raise Http404("Resume file not found on server.")

    return FileResponse(open(file_path, 'rb'), as_attachment=True,
                        filename=os.path.basename(file_path))
