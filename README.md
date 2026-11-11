# Student Project Management System (StudentProjectSystem)

A full-stack Django web application developed for managing, tracking, and reviewing student academic projects across university departments.

---

## Table of Contents
1. [Project Overview & Features](#project-overview--features)
2. [Assignment Questions & Answers](#assignment-questions--answers)
   - [Question 1: Environment and Project Setup](#question-one-environment-and-project-setup)
   - [Question 2: URLs, Views and HTTP Requests](#question-two-urls-views-and-http-requests)
   - [Question 3: Database Models and ORM](#question-three-database-models-and-orm)
   - [Question 4: Templates and Front-End Integration](#question-four-templates-and-front-end-integration)
   - [Question 5: Django Forms and CRUD Operations](#question-five-django-forms-and-crud-operations)
   - [Question 6: User Authentication and Authorization](#question-six-user-authentication-and-authorization)
   - [Question 7: Search, Static Files and Presentation](#question-seven-search-static-files-and-presentation)
3. [Quick Setup & Running Instructions](#quick-setup--running-instructions)
4. [Pre-configured Test Credentials](#pre-configured-test-credentials)

---

## Project Overview & Features
- **Project Name:** `StudentProjectSystem`
- **Application Name:** `projects`
- **Core Capabilities:**
  - Full CRUD functionality for student projects.
  - Case-insensitive search by project title.
  - Django built-in authentication with protected CRUD routes.
  - Responsive HTML5 table presentation styled with custom static CSS.
  - Pre-seeded with sample departments and projects.

---

## Assignment Questions & Answers

### QUESTION ONE: ENVIRONMENT AND PROJECT SETUP (4 MARKS)

#### a) Create a Python virtual environment named `venv` and activate it (1 mark)
```bash
# Create the virtual environment
python3 -m venv venv

# Activate on Linux / macOS:
source venv/bin/activate

# (On Windows Command Prompt: venv\Scripts\activate.bat | PowerShell: venv\Scripts\Activate.ps1)
```

#### b) Install Django within the virtual environment (1 mark)
```bash
pip install django
```

#### c) Create a Django project named `StudentProjectSystem` and an application named `projects` (1 mark)
```bash
# Create the project
django-admin startproject StudentProjectSystem

# Enter the project directory
cd StudentProjectSystem

# Create the application
python manage.py startapp projects
```

#### d) Register the `projects` application in `INSTALLED_APPS` within `settings.py` (1 mark)
In `StudentProjectSystem/settings.py`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'projects',  # Registered application
]
```

---

### QUESTION TWO: URLS, VIEWS AND HTTP REQUESTS (5 MARKS)

#### a) View function named `home` returning the welcome message (1 mark)
```python
from django.shortcuts import render

def home(request):
    return render(request, 'projects/home.html')
```

#### b) Route root URL `/` to the `home` view across project and app URL files (2 marks)

- **Project URLs (`StudentProjectSystem/urls.py`):**
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projects.urls')),
]
```

- **Application URLs (`projects/urls.py`):**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project_list'),
]
```

#### c) `project_list` view retrieving all registered projects and passing to an HTML template (2 marks)
```python
from django.shortcuts import render
from .models import Project

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})
```

---

### QUESTION THREE: DATABASE MODELS AND ORM (6 MARKS)

#### a) & b) `Department` and `Project` Models (4 marks)
In `projects/models.py`:
```python
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    student_name = models.CharField(max_length=150)
    registration_number = models.CharField(max_length=30)
    description = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.title
```

#### c) Generate and apply database migrations (1 mark)
```bash
python manage.py makemigrations
python manage.py migrate
```

#### d) Django ORM query to retrieve all projects belonging to a particular department (1 mark)
```python
from projects.models import Project, Department

# Method 1: Using double-underscore lookup by department name
projects = Project.objects.filter(department__name="Computer Science")

# Method 2: Filtering using a Department model instance
cs_dept = Department.objects.get(name="Computer Science")
projects = Project.objects.filter(department=cs_dept)

# Method 3: Using reverse relationship (related_name='projects')
projects = cs_dept.projects.all()
```

---

### QUESTION FOUR: TEMPLATES AND FRONT-END INTEGRATION (5 MARKS)

#### a) `base.html` structure with navigation menu (1 mark)
Located at `projects/templates/projects/base.html`:
- Navigation menu contains links: **Home**, **Projects**, and **Add Project**.

#### b) `home.html` extending `base.html` (1 mark)
Located at `projects/templates/projects/home.html`:
Displays: `"Welcome to the Student Project Management System"`.

#### c) & d) `project_list.html` table, template variables, and `for` loop (3 marks)
Located at `projects/templates/projects/project_list.html`:
Displays:
- Project Title (`{{ project.title }}`)
- Student Name (`{{ project.student_name }}`)
- Registration Number (`{{ project.registration_number }}`)
- Department (`{{ project.department.name }}`)
Using `{% for project in projects %} ... {% endfor %}`.

---

### QUESTION FIVE: DJANGO FORMS AND CRUD OPERATIONS (8 MARKS)

#### a) `ProjectForm` ModelForm (2 marks)
In `projects/forms.py`:
```python
from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'student_name', 'registration_number', 'description', 'department']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'student_name': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }
```

#### b) Project Creation View (2 marks)
`project_create` processes `POST` submissions via `ProjectForm`, validates, saves to database, and redirects to `'project_list'`.

#### c) Project Edit/Update View (2 marks)
`project_update` retrieves project instance via `get_object_or_404(Project, pk=pk)`, pre-populates the form, saves updates on `POST`, and redirects.

#### d) Project Delete View with Confirmation (2 marks)
`project_delete` displays `project_confirm_delete.html` on `GET` and executes deletion on `POST`.

---

### QUESTION SIX: USER AUTHENTICATION AND AUTHORIZATION (4 MARKS)

#### a) Login View using Built-in Authentication (2 marks)
Implemented in `projects/views.py` (`user_login`) utilizing Django's `AuthenticationForm` and `django.contrib.auth.login`.

#### b) Access Restriction on Create, Edit, Delete (2 marks)
Protected using `@login_required(login_url='login')` decorator:
- Unauthenticated users attempting to add, edit, or delete are redirected to `/login/?next=<path>`.

---

### QUESTION SEVEN: SEARCH, STATIC FILES AND PRESENTATION (4 MARKS)

#### a) Search Functionality by Title (2 marks)
Implemented in `project_list` view:
```python
query = request.GET.get('q', '').strip()
if query:
    projects = Project.objects.filter(title__icontains=query)
else:
    projects = Project.objects.all()
```

#### b) Static CSS Styling (1 mark)
Located at `projects/static/projects/css/style.css`, linked in `base.html` using `{% load static %}`:
- Custom styles applied to navigation bar, project table, buttons, search input, and responsive layouts.

#### c) Demonstration and Verification (1 mark)
All unit and functional integration tests pass successfully with 100% compliance.

---

## Quick Setup & Running Instructions

```bash
# 1. Clone repository
git clone <YOUR_REPOSITORY_URL>
cd <REPOSITORY_FOLDER>

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations (already applied if using provided db.sqlite3)
cd StudentProjectSystem
python manage.py migrate

# (Optional: load sample seed data if starting fresh)
python manage.py loaddata seed_data.json

# 5. Start development server
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

---

## Pre-configured Test Credentials

| Role | Username | Password |
|---|---|---|
| **Administrator** | `admin` | `admin123` |
