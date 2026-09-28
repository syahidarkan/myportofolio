import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from main.models import Experience, Project
from main.forms import ExperienceForm, ProjectForm


def is_editor(user):
    return user.groups.filter(name="Editor").exists()


def show_main(request):
    last_login = request.COOKIES.get("last_login", "Belum ada sesi login / Cookie tidak ditemukan")
    context = {
        "name": "Syahid Arkan Fashihurrohman",
        "npm": "2506632936",
        "study_program": "S1 Sistem Informasi",
        "bio": "Information Systems @ Universitas Indonesia. Building PandaTech.",
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")
    context = {
        "name": "Syahid Arkan Fashihurrohman",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie("last_login", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return response
    context = {
        "name": "Syahid Arkan Fashihurrohman",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response


def show_experience(request):
    json_response = get_experience_json(request)
    experiences = serializers.deserialize("json", json_response.content.decode("utf-8"))
    context = {
        "name": "Syahid Arkan Fashihurrohman",
        "experience_list": [experience.object for experience in experiences],
        "active_page": "experience",
        "is_editor": is_editor(request.user),
    }
    return render(request, "experience.html", context)


def get_experience_json(request):
    experiences = Experience.objects.all()
    return HttpResponse(serializers.serialize("json", experiences), content_type="application/json")


def get_experience_xml(request):
    experiences = Experience.objects.all()
    return HttpResponse(serializers.serialize("xml", experiences), content_type="application/xml")


@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")
    context = {
        "name": "Syahid Arkan Fashihurrohman",
        "form": form,
        "form_title": "Tambah pengalaman",
        "form_subtitle": "Tambahin pengalaman baru ke portofolio.",
        "cancel_url": "main:show_experience",
        "active_page": "experience",
    }
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied

    experience = get_object_or_404(Experience, id=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")
    context = {
        "name": "Syahid Arkan Fashihurrohman",
        "form": form,
        "form_title": "Edit pengalaman",
        "form_subtitle": experience.title,
        "cancel_url": "main:show_experience",
        "active_page": "experience",
    }
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, id=experience_id)
    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
    return redirect("main:show_experience")


def show_projects(request):
    json_response = get_projects_json(request)
    projects = serializers.deserialize("json", json_response.content.decode("utf-8"))
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()
    context = {
        "name": "Syahid Arkan Fashihurrohman",
        "project_list": projects,
        "title_query": title_query,
        "active_page": "projects",
        "is_editor": is_editor(request.user),
    }
    return render(request, "projects.html", context)


def show_project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    context = {
        "name": "Syahid Arkan Fashihurrohman",
        "project": project,
        "active_page": "projects",
    }
    return render(request, "project_detail.html", context)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()
    if title_query:
        projects = projects.filter(name__icontains=title_query)
    projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True)
    return HttpResponse(projects_json, content_type="application/json")


def get_projects_xml(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()
    if title_query:
        projects = projects.filter(name__icontains=title_query)
    projects_xml = serializers.serialize("xml", projects, use_natural_foreign_keys=True)
    return HttpResponse(projects_xml, content_type="application/xml")


@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")
    context = {
        "name": "Syahid Arkan Fashihurrohman",
        "form": form,
        "form_title": "Tambah proyek",
        "form_subtitle": "Tambahin proyek baru ke daftar portofolio.",
        "cancel_url": "main:show_projects",
        "active_page": "projects",
    }
    return render(request, "projects_form.html", context)


@login_required(login_url="/login/")
def update_project(request, project_id):
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied

    project = get_object_or_404(Project, id=project_id)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_projects")
    context = {
        "name": "Syahid Arkan Fashihurrohman",
        "form": form,
        "form_title": "Edit proyek",
        "form_subtitle": project.name,
        "cancel_url": "main:show_projects",
        "active_page": "projects",
    }
    return render(request, "projects_form.html", context)


@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
    return redirect("main:show_projects")


@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)
    return redirect("main:show_projects")
