# Hirewise — Job Portal (Django Version)

A full-stack Job Portal web application built entirely on **Django (Python)** with **HTML/CSS/Vanilla JS** for the frontend templates.

---

## Project Structure

```
Django-Hirewise/
├── accounts/           ← Django app handling Users (Applicants/Recruiters) and Auth
├── jobs/               ← Django app handling Job Postings and Applications
├── hirewise/           ← Core Django project settings & routing
├── templates/          ← Global HTML templates for both apps
├── static/             ← Custom CSS stylesheets, Javascript, and images
├── media/              ← User uploaded files (resumes, etc.)
├── manage.py           ← Django CLI utility
└── README.md
```

---

## Setup Instructions

### 1. Prerequisites
Make sure you have **Python 3.8+** installed.

### 2. Create a Virtual Environment
It is recommended to run this project inside a Python virtual environment to keep dependencies clean.
```bash
# Create the virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies
Install all required Python packages specifically logged in the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

### 4. Database Setup
Django handles the database schema entirely through Python models. Run the migrations to build your SQLite database automatically:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Project
Start the Django development server:
```bash
python manage.py runserver
```

The application will now be running continuously at **http://127.0.0.1:8000/**

---

## Features

### Applicant Portal
- Register & create an applicant profile
- Browse a feed of open job listings
- Apply for jobs and upload resumes directly
- Track exactly which jobs have been applied for

### Recruiter Portal
- Register as a company recruiter
- Post new job vacancies specifying role, domain, and salary
- Seamless login routing depending on user role

---

## Tech Stack
- **Backend & Routing**: Django (Python)
- **Database**: SQLite (Default via Django ORM)
- **Frontend**: Django Templates, Vanilla HTML5, CSS3, ES6 JavaScript
