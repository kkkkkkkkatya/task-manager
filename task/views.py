from django.shortcuts import render

from .models import Project, Team, Worker


def index(request):
    """View function for home page."""
    num_projects = Project.objects.count()
    num_teams = Team.objects.count()
    num_workers = Worker.objects.count()

    context = {
        "num_projects": num_projects,
        "num_teams": num_teams,
        "num_workers": num_workers,
    }

    return render(request, "task/index.html", context=context)
