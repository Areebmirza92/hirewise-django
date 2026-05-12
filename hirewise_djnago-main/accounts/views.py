"""
accounts/views.py — Login, Register, Logout, Profile
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, ApplicantRegistrationForm, RecruiterRegistrationForm
from .models import User


def auth_view(request):
    """
    Main auth page — handles both Login and Register for Applicants & Recruiters.
    GET:  render the auth page with empty forms
    POST: handle login OR register based on hidden 'form_type' field
    """
    login_form = LoginForm()
    applicant_form = ApplicantRegistrationForm()
    recruiter_form = RecruiterRegistrationForm()

    # Which tab / role to show after re-render on error
    active_tab = 'login'
    active_role = 'applicant'

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        active_role = request.POST.get('active_role', 'applicant')

        # ── LOGIN ────────────────────────────────────────────
        if form_type == 'login':
            active_tab = 'login'
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = login_form.cleaned_data['user']
                login(request, user)
                if user.role == 'recruiter':
                    return redirect('post_job')
                return redirect('browse_jobs')
            # form errors fall through to re-render

        # ── REGISTER APPLICANT ───────────────────────────────
        elif form_type == 'register_applicant':
            active_tab = 'register'
            active_role = 'applicant'
            applicant_form = ApplicantRegistrationForm(request.POST, request.FILES)
            if applicant_form.is_valid():
                user = applicant_form.save()
                login(request, user)
                messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
                return redirect('browse_jobs')

        # ── REGISTER RECRUITER ───────────────────────────────
        elif form_type == 'register_recruiter':
            active_tab = 'register'
            active_role = 'recruiter'
            recruiter_form = RecruiterRegistrationForm(request.POST)
            if recruiter_form.is_valid():
                user = recruiter_form.save()
                login(request, user)
                messages.success(request, f'Welcome, {user.first_name}! Your recruiter account is ready.')
                return redirect('post_job')

    return render(request, 'accounts/auth.html', {
        'login_form': login_form,
        'applicant_form': applicant_form,
        'recruiter_form': recruiter_form,
        'active_tab': active_tab,
        'active_role': active_role,
    })


def logout_view(request):
    """Log out the current user and redirect to login."""
    logout(request)
    return redirect('auth')


@login_required
def profile_view(request):
    """Applicant profile page — shows and allows updating profile & resume."""
    user = request.user
    if user.role != 'applicant':
        return redirect('post_job')

    if request.method == 'POST':
        form = ApplicantRegistrationForm(request.POST, request.FILES, instance=user)
        # Remove password requirement for profile update
        form.fields['password'].required = False
        if form.is_valid():
            obj = form.save(commit=False)
            new_pw = form.cleaned_data.get('password')
            if new_pw:
                obj.set_password(new_pw)
            obj.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ApplicantRegistrationForm(instance=user)
        form.fields['password'].required = False

    return render(request, 'accounts/profile.html', {'form': form})
