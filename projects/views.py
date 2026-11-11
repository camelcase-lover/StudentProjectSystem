from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Project, Department
from .forms import ProjectForm

# QUESTION TWO (a) & QUESTION FOUR (b): Home View
def home(request):
    """Displays the welcome message using home.html extending base.html."""
    return render(request, 'projects/home.html')


# QUESTION TWO (c), QUESTION FOUR (c, d) & QUESTION SEVEN (a): Project List & Search View
def project_list(request):
    """
    Retrieves all projects from the database or filters them by project title
    if a search query is provided.
    """
    query = request.GET.get('q', '').strip()
    if query:
        projects = Project.objects.filter(title__icontains=query)
    else:
        projects = Project.objects.all()

    context = {
        'projects': projects,
        'query': query,
    }
    return render(request, 'projects/project_list.html', context)


# QUESTION FIVE (b) & QUESTION SIX (b): Create Project View
@login_required(login_url='login')
def project_create(request):
    """Enables authenticated users to submit a new project."""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()

    return render(request, 'projects/project_form.html', {
        'form': form,
        'title': 'Add New Project',
        'button_text': 'Submit Project',
    })


# QUESTION FIVE (c) & QUESTION SIX (b): Edit/Update Project View
@login_required(login_url='login')
def project_update(request, pk):
    """Enables authenticated users to edit and update an existing project."""
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/project_form.html', {
        'form': form,
        'title': 'Edit Project',
        'button_text': 'Update Project',
        'project': project,
    })


# QUESTION FIVE (d) & QUESTION SIX (b): Delete Project View
@login_required(login_url='login')
def project_delete(request, pk):
    """
    Displays a confirmation page before deletion,
    and deletes the project upon confirmation (POST).
    """
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')

    return render(request, 'projects/project_confirm_delete.html', {
        'project': project,
    })


# QUESTION SIX (a): Login View using Django's built-in authentication system
def user_login(request):
    """Authenticates user using Django's built-in AuthenticationForm."""
    if request.user.is_authenticated:
        return redirect('project_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'project_list')
            return redirect(next_url)
    else:
        form = AuthenticationForm()

    return render(request, 'projects/login.html', {'form': form})


# Logout View
def user_logout(request):
    """Logs out the user and redirects to home."""
    logout(request)
    return redirect('home')
