from django.shortcuts import render, get_object_or_404

from main.models import Experience, Project


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
    }
    return render(request, "experience.html", context)


def show_projects(request):
    context = {
        "name": "Syahid Arkan Fashihurrohman",
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)


def show_project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    context = {
        "name": "Syahid Arkan Fashihurrohman",
        "project": project,
    }
    return render(request, "project_detail.html", context)
