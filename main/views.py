from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from main.models import Experience, Project
from main.forms import ExperienceForm, ProjectForm


def show_main(request):
    context = {
        "name": "Syahid Arkan Fashihurrohman",
        "npm": "2506632936",
        "study_program": "S1 Sistem Informasi",
        "bio": "Information Systems @ Universitas Indonesia. Building PandaTech.",
    }
    return render(request, "index.html", context)


def show_experience(request):
    # sama kayak show_projects: ambil lewat endpoint JSON dulu, baru di-deserialize
    json_response = get_experience_json(request)
    experiences = serializers.deserialize("json", json_response.content.decode("utf-8"))
    context = {
        "name": "Syahid Arkan Fashihurrohman",
        "experience_list": [experience.object for experience in experiences],
        "active_page": "experience",
    }
    return render(request, "experience.html", context)


def get_experience_json(request):
    experiences = Experience.objects.all()
    return HttpResponse(serializers.serialize("json", experiences), content_type="application/json")


def get_experience_xml(request):
    experiences = Experience.objects.all()
    return HttpResponse(serializers.serialize("xml", experiences), content_type="application/xml")


def create_experience(request):
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


def update_experience(request, experience_id):
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


def delete_experience(request, experience_id):
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
    # dipakai show_projects sendiri buat ambil data, sekalian jadi endpoint publik
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()
    if title_query:
        projects = projects.filter(name__icontains=title_query)
    return HttpResponse(serializers.serialize("json", projects), content_type="application/json")


def get_projects_xml(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()
    if title_query:
        projects = projects.filter(name__icontains=title_query)
    return HttpResponse(serializers.serialize("xml", projects), content_type="application/xml")


def create_project(request):
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


def update_project(request, project_id):
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


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
    return redirect("main:show_projects")
