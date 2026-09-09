from django.shortcuts import render

from main.models import Experience


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
