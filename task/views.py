from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

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


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    context_object_name = "project_list"
    template_name = "task/project_list.html"
    paginate_by = 5

    def get_queryset(self):
        return Project.objects.prefetch_related("teams")


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
