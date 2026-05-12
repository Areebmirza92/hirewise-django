"""
accounts/forms.py — Authentication & Registration forms for Hirewise
"""

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User


# ── Login Form ────────────────────────────────────────────────
class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com', 'id': 'login-email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'id': 'login-password'})
    )
    role = forms.ChoiceField(
        choices=[('applicant', 'Applicant'), ('recruiter', 'Recruiter')],
        widget=forms.HiddenInput(attrs={'id': 'login-role'})
    )

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get('email')
        password = cleaned.get('password')
        role = cleaned.get('role')

        if email and password and role:
            try:
                user_obj = User.objects.get(email=email, role=role)
            except User.DoesNotExist:
                raise forms.ValidationError('Invalid credentials or wrong role selected.')

            user = authenticate(username=user_obj.username, password=password)
            if user is None:
                raise forms.ValidationError('Invalid credentials.')

            cleaned['user'] = user
        return cleaned


# ── Applicant Registration Form ───────────────────────────────
class ApplicantRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': 'Min. 6 characters', 'id': 'reg-password'})
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'password',
            'phone', 'address',
            'position_applied_for', 'experience', 'skills', 'certifications',
            'domain', 'resume',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'id': 'reg-first-name'}),
            'last_name':  forms.TextInput(attrs={'placeholder': 'Last Name',  'id': 'reg-last-name'}),
            'email':      forms.EmailInput(attrs={'placeholder': 'you@example.com', 'id': 'reg-email'}),
            'phone':      forms.TextInput(attrs={'placeholder': '+91 98765 43210', 'id': 'reg-phone'}),
            'address':    forms.Textarea(attrs={'rows': 2, 'placeholder': '123 Main St, City, Country', 'id': 'reg-address'}),
            'position_applied_for': forms.TextInput(attrs={'placeholder': 'e.g. Frontend Engineer', 'id': 'reg-position'}),
            'experience': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe your work experience…', 'id': 'reg-experience'}),
            'skills':     forms.TextInput(attrs={'placeholder': 'e.g. React, Excel, Strategy', 'id': 'reg-skills'}),
            'certifications': forms.TextInput(attrs={'placeholder': 'e.g. AWS Certified, PMP', 'id': 'reg-certifications'}),
            'domain':     forms.Select(attrs={'id': 'reg-domain'}),
            'resume':     forms.FileInput(attrs={'id': 'reg-resume', 'accept': '.pdf,.doc,.docx'}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name':  'Last Name',
            'position_applied_for': 'Position Applying For',
            'domain': 'Industry / Domain',
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            ext = resume.name.split('.')[-1].lower()
            if ext not in ['pdf', 'doc', 'docx']:
                raise forms.ValidationError('Only PDF, DOC, or DOCX files are allowed.')
            if resume.size > 5 * 1024 * 1024:   # 5 MB max
                raise forms.ValidationError('Resume file must be smaller than 5 MB.')
        return resume

    def save(self, commit=True):
        user = super().save(commit=False)
        raw_pw = self.cleaned_data['password']
        # Build username from email prefix
        base_username = self.cleaned_data['email'].split('@')[0]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        user.username = username
        user.role = 'applicant'
        user.set_password(raw_pw)
        if commit:
            user.save()
        return user


# ── Recruiter Registration Form ───────────────────────────────
class RecruiterRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': 'Min. 6 characters', 'id': 'reg-password'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'domain']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'id': 'reg-first-name'}),
            'last_name':  forms.TextInput(attrs={'placeholder': 'Last Name',  'id': 'reg-last-name'}),
            'email':      forms.EmailInput(attrs={'placeholder': 'you@example.com', 'id': 'reg-email'}),
            'domain':     forms.Select(attrs={'id': 'reg-domain'}),
        }
        labels = {
            'domain': 'Industry / Domain',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        raw_pw = self.cleaned_data['password']
        base_username = self.cleaned_data['email'].split('@')[0]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        user.username = username
        user.role = 'recruiter'
        user.set_password(raw_pw)
        if commit:
            user.save()
        return user
