from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from main.models import Experience, Project
from main.forms import ProjectForm


def show_main(request):
    context = {
        "name": "Syahid Arkan Fashihurrohman",
        "npm": "2506632936",
        "study_program": "S1 Sistem Informasi",
        "bio": "Information Systems @ Universitas Indonesia. Building PandaTech.",
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Syahid Arkan Fashihurrohman",
        "experience_list": Experience.objects.all(),
        "active_page": "experience",
    }
    return render(request, "experience.html", context)


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
    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")


def get_projects_xml(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()
    if title_query:
        projects = projects.filter(name__icontains=title_query)
    projects_xml = serializers.serialize("xml", projects)
    return HttpResponse(projects_xml, content_type="application/xml")


def create_project(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")
    context = {
        "name": "Syahid Arkan Fashihurrohman",
        "form": form,
        "active_page": "projects",
    }
    return render(request, "projects_form.html", context)


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")
    return redirect("main:show_projects")
