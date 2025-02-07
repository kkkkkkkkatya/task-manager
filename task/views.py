from django.contrib.auth import logout
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import json

from .forms import TaskForm, TeamForm
from .models import Project, Team, Worker, Task


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
    """View class for projects page."""
    model = Project
    context_object_name = "project_list"
    template_name = "task/project_list.html"

    def get_queryset(self):
        return Project.objects.prefetch_related("teams")


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    """View class for project page."""
    model = Project


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    """View class for project create page."""
    model = Project
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("task:project-detail", kwargs={"pk": self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    """View class for project update page."""
    model = Project
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("task:project-detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    """View class for project delete."""
    model = Project
    success_url = reverse_lazy("task:project-list")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    """View class for task create page."""
    model = Task
    form_class = TaskForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        project = get_object_or_404(Project, pk=self.kwargs["pk"])
        kwargs["project"] = project
        return kwargs

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs["pk"])
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("task:project-detail", kwargs={"pk": self.object.project.pk})


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    """View class for task update page."""
    model = Task
    form_class = TaskForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        task = get_object_or_404(Task, pk=self.kwargs["pk"])
        kwargs["project"] = task.project
        return kwargs

    def get_success_url(self):
        return reverse_lazy("task:project-detail", kwargs={"pk": self.object.project.pk})

    # Handle AJAX requests for updating is_completed field
    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return self.handle_ajax(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def handle_ajax(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            print("Received Data:", data)
            task = get_object_or_404(Task, pk=self.kwargs["pk"])
            task.is_completed = bool(data.get("is_completed"))
            task.save()
            return JsonResponse({"success": True, "is_completed": task.is_completed})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)


class TaskDeleteView(LoginRequiredMixin, View):
    """View class for task delete."""
    def post(self, request, pk, *args, **kwargs):
        task = Task.objects.get(pk=pk)
        project_pk = task.project.pk
        task.delete()
        return redirect(reverse_lazy("task:project-detail", kwargs={"pk": project_pk}))


class TeamListView(LoginRequiredMixin, generic.ListView):
    """View class for teams page."""
    model = Team
    context_object_name = "team_list"
    template_name = "task/team_list.html"

    def get_queryset(self):
        return Team.objects.annotate(worker_count=Count('members')).prefetch_related("members")


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    """View class for team page."""
    model = Team
    template_name = "task/team_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.object
        context['team_members'] = team.members.all()
        context['projects'] = Project.objects.filter(teams=team)

        return context


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    """View class for team create page."""
    model = Team
    form_class = TeamForm

    def get_success_url(self):
        return reverse_lazy("task:team-detail", kwargs={"pk": self.object.pk})


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    """View class for team update page."""
    model = Team
    form_class = TeamForm

    def get_success_url(self):
        return reverse_lazy("task:team-detail", kwargs={"pk": self.object.pk})


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    """View class for team delete."""
    model = Team
    success_url = reverse_lazy("task:team-list")


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    """View class for worker/user profile page."""
    model = Worker
    template_name = "task/worker_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.object
        context['worker_teams'] = worker.teams.all()

        return context


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    """View class for worker/user profile update page."""
    model = Worker
    fields = ["username", "first_name", "last_name", "position", "email"]

    def get_success_url(self):
        return reverse_lazy("task:worker-detail", kwargs={"pk": self.object.pk})


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    """View class for worker/user profile dalete."""
    model = Worker
    success_url = reverse_lazy("task:index")

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            logout(request)  # Log out the user before deletion
        return super().delete(request, *args, **kwargs)
