"""
jobs/management/commands/seed_data.py
Run with: python manage.py seed_data

Seeds the database with:
  - 4 Recruiters (password: password123)
  - 3 Applicants (password: password123)
  - 9 Jobs across domains
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from jobs.models import Job

User = get_user_model()

RECRUITERS = [
    {'first_name': 'Google',   'last_name': 'HR',      'email': 'recruiter@google.com',   'domain': 'Technology'},
    {'first_name': 'Goldman',  'last_name': 'Finance',  'email': 'recruiter@goldman.com',  'domain': 'Finance'},
    {'first_name': 'Netflix',  'last_name': 'Studios',  'email': 'recruiter@netflix.com',  'domain': 'Media'},
    {'first_name': 'Amazon',   'last_name': 'Ops',      'email': 'recruiter@amazon.com',   'domain': 'E-Commerce'},
]

APPLICANTS = [
    {
        'first_name': 'Alice', 'last_name': 'Johnson', 'email': 'alice@example.com',
        'domain': 'Technology', 'skills': 'React, TypeScript, Node.js',
        'experience': '4 years in frontend development',
        'position_applied_for': 'Frontend Engineer',
        'phone': '+1 555-0101', 'address': '42 Code Lane, San Francisco, CA',
        'certifications': 'AWS Certified Developer',
    },
    {
        'first_name': 'Bob', 'last_name': 'Smith', 'email': 'bob@example.com',
        'domain': 'Finance', 'skills': 'Financial Analysis, Excel, Python',
        'experience': '3 years as an analyst',
        'position_applied_for': 'Investment Analyst',
        'phone': '+1 555-0102', 'address': '7 Wall Street, New York, NY',
        'certifications': 'CFA Level 1',
    },
    {
        'first_name': 'Carol', 'last_name': 'White', 'email': 'carol@example.com',
        'domain': 'Media', 'skills': 'Figma, Adobe Creative Suite, Sketch',
        'experience': '5 years in UX/UI design',
        'position_applied_for': 'UX Designer',
        'phone': '+1 555-0103', 'address': '15 Creative Blvd, Los Angeles, CA',
        'certifications': 'Google UX Design Certificate',
    },
]

JOBS = [
    {'title': 'Frontend Engineer',
     'description': 'Build responsive web applications using React and TypeScript. Collaborate with designers and backend engineers. 3+ years experience required.',
     'domain': 'Technology', 'recruiter_email': 'recruiter@google.com'},
    {'title': 'Backend Engineer',
     'description': 'Design and maintain scalable APIs using Go and gRPC. Work on high-throughput distributed systems. 4+ years experience.',
     'domain': 'Technology', 'recruiter_email': 'recruiter@google.com'},
    {'title': 'Data Scientist',
     'description': 'Apply ML models to search and recommendation systems. Proficiency in Python, TensorFlow, and SQL required.',
     'domain': 'Technology', 'recruiter_email': 'recruiter@google.com'},
    {'title': 'Investment Analyst',
     'description': 'Conduct financial modelling, sector research, and market analysis for equity portfolios. CFA Level 1 preferred.',
     'domain': 'Finance', 'recruiter_email': 'recruiter@goldman.com'},
    {'title': 'Risk Manager',
     'description': 'Monitor and manage credit, market, and operational risk. Develop risk frameworks. 5+ years in banking required.',
     'domain': 'Finance', 'recruiter_email': 'recruiter@goldman.com'},
    {'title': 'Content Producer',
     'description': 'Develop original content strategies and manage end-to-end video production. Experience with streaming platforms preferred.',
     'domain': 'Media', 'recruiter_email': 'recruiter@netflix.com'},
    {'title': 'UX Designer',
     'description': 'Create wireframes, prototypes, and final designs for Netflix product features. Mastery of Figma required.',
     'domain': 'Media', 'recruiter_email': 'recruiter@netflix.com'},
    {'title': 'Supply Chain Manager',
     'description': 'Oversee end-to-end supply chain operations for Amazon fulfilment centres. SAP experience required. 6+ years in logistics.',
     'domain': 'E-Commerce', 'recruiter_email': 'recruiter@amazon.com'},
    {'title': 'Product Manager',
     'description': 'Define product vision, write PRDs, and lead cross-functional teams to launch new marketplace features. 4+ years in product management.',
     'domain': 'E-Commerce', 'recruiter_email': 'recruiter@amazon.com'},
]


class Command(BaseCommand):
    help = 'Seed the database with sample recruiters, applicants, and job listings'

    def handle(self, *args, **options):
        self.stdout.write('[*] Seeding database...\n')

        # ── Create Recruiters ──────────────────────────────
        recruiter_objs = {}
        for r in RECRUITERS:
            username = r['email'].replace('@', '_at_').replace('.', '_')
            user, created = User.objects.get_or_create(
                email=r['email'],
                defaults={
                    'username': username,
                    'first_name': r['first_name'],
                    'last_name': r['last_name'],
                    'role': 'recruiter',
                    'domain': r['domain'],
                    'is_active': True,
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'  [OK] Created recruiter: {user.email}')
            else:
                self.stdout.write(f'  [--] Recruiter already exists: {user.email}')
            recruiter_objs[r['email']] = user

        # ── Create Applicants ──────────────────────────────
        for a in APPLICANTS:
            username = a['email'].replace('@', '_at_').replace('.', '_')
            user, created = User.objects.get_or_create(
                email=a['email'],
                defaults={
                    'username': username,
                    'first_name': a['first_name'],
                    'last_name': a['last_name'],
                    'role': 'applicant',
                    'domain': a['domain'],
                    'skills': a['skills'],
                    'experience': a['experience'],
                    'position_applied_for': a.get('position_applied_for', ''),
                    'phone': a.get('phone', ''),
                    'address': a.get('address', ''),
                    'certifications': a.get('certifications', ''),
                    'is_active': True,
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'  [OK] Created applicant: {user.email}')
            else:
                self.stdout.write(f'  [--] Applicant already exists: {user.email}')

        # ── Create Jobs ────────────────────────────────────
        for j in JOBS:
            recruiter = recruiter_objs.get(j['recruiter_email'])
            job, created = Job.objects.get_or_create(
                title=j['title'],
                recruiter=recruiter,
                defaults={
                    'description': j['description'],
                    'domain': j['domain'],
                }
            )
            if created:
                self.stdout.write(f'  [OK] Created job: {job.title}')
            else:
                self.stdout.write(f'  [--] Job already exists: {job.title}')

        self.stdout.write(self.style.SUCCESS('\n[DONE] Seeding complete! All accounts use password: password123\n'))
