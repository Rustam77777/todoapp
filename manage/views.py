from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import SignUpForm, ProjectForm, TaskForm, UserProfileForm, ProfileForm, PasswordForm
from .models import Project, Task
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f"Account created for {user.username}! You can now log in."
            )
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'manage/signup.html', {'form': form})


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'manage/dashboard.html'


# check admin user
is_admin = lambda u: u.is_staff

@login_required
@user_passes_test(is_admin)
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'manage/project_create.html', {'form': form})

@login_required
def project_list(request):
    user = request.user
    if user.is_staff:
        projects = Project.objects.all()
    else:
        # only projects where user is assigned to at least one task
        projects = Project.objects.filter(tasks__assignees=user).distinct()

    return render(request, 'manage/project_list.html', {'projects': projects})

@login_required
def task_update_status(request, pk):
    task = get_object_or_404(Task, pk=pk, assignee=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
    return redirect('project_list')

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    # restrict members to assigned projects
    if not request.user.is_staff and not project.tasks.filter(assignees=request.user).exists():
        return redirect('project_list')
    return render(request, 'manage/project_detail.html', {'project': project})

@login_required
@user_passes_test(is_admin)
def task_create(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            form.save_m2m()
            return redirect('project_detail', pk=project.id)
    else:
        form = TaskForm()
    return render(request, 'manage/task_create.html', {'form': form, 'project': project})

@login_required
def task_update_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
    return redirect('project_list')

@login_required
@user_passes_test(is_admin)
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        messages.success(request, 'Project updated successfully.')
        return redirect('project_detail', pk=project.id)
    return render(request, 'manage/project_create.html', {'form': form, 'project': project})

@login_required
@user_passes_test(is_admin)
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted.')
        return redirect('project_list')
    return render(request, 'manage/project_confirm_delete.html', {'project': project})

@login_required
@user_passes_test(is_admin)
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        
        messages.success(request, 'Task updated successfully.')
        return redirect('project_detail', task.project.id)
    # pass project into template context for back-link
    return render(request, 'manage/task_create.html', {
        'form': form,
        'task': task,
        'project': task.project,
    })

@login_required
@user_passes_test(is_admin)
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project_id = task.project.id
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted.')
        return redirect('project_detail', pk=project_id)
    return render(request, 'manage/task_confirm_delete.html', {'task': task})

@login_required
def profile_edit(request):
    user     = request.user
    u_form   = UserProfileForm(request.POST or None, instance=user)
    p_form   = ProfileForm(request.POST or None, request.FILES or None, instance=user.profile)
    pwd_form = PasswordForm(user, request.POST or None)

    if request.method == 'POST':
        # Profile update
        if 'save_profile' in request.POST and u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated.')
            return redirect('project_list')

        # Password change
        if 'change_password' in request.POST and pwd_form.is_valid():
            user = pwd_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed.')
            return redirect('project_list')

    return render(request, 'manage/profile_edit.html', {
        'u_form': u_form,
        'p_form': p_form,
        'pwd_form': pwd_form,
    })