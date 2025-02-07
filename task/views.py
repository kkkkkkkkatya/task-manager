from django.contrib.auth import logout
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
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
    model = Project
    context_object_name = "project_list"
    template_name = "task/project_list.html"
    paginate_by = 5

    def get_queryset(self):
        return Project.objects.prefetch_related("teams")


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("task:project-detail", kwargs={"pk": self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("task:project-detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("task:project-list")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        project = get_object_or_404(Project, pk=self.kwargs["pk"])
        kwargs["project"] = project  # Pass project to form
        return kwargs

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs["pk"])
        form.instance.project = project  # Automatically assign project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("task:project-detail", kwargs={"pk": self.object.project.pk})


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        task = get_object_or_404(Task, pk=self.kwargs["pk"])
        kwargs["project"] = task.project
        return kwargs

    def get_success_url(self):
        return reverse_lazy("task:project-detail", kwargs={"pk": self.object.project.pk})

    # Handle AJAX requests for updating is_completed
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
    def post(self, request, pk, *args, **kwargs):
        task = Task.objects.get(pk=pk)
        project_pk = task.project.pk  # Get project ID before deleting
        task.delete()
        return redirect(reverse_lazy("task:project-detail", kwargs={"pk": project_pk}))


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    context_object_name = "team_list"
    template_name = "task/team_list.html"
    paginate_by = 5

    def get_queryset(self):
        return Team.objects.annotate(worker_count=Count('members')).prefetch_related("members")


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    template_name = "task/team_detail.html"  # Update to your actual template path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.object

        # Get team members
        context['team_members'] = team.members.all()  # Get all workers in the team

        # Get projects associated with the team
        context['projects'] = Project.objects.filter(teams=team)  # Get all projects this team is working on

        return context


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamForm

    def get_success_url(self):
        return reverse_lazy("task:team-detail", kwargs={"pk": self.object.pk})


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamForm

    def get_success_url(self):
        return reverse_lazy("task:team-detail", kwargs={"pk": self.object.pk})


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("task:team-list")


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = "task/worker_detail.html"  # Update to your actual template path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.object
        context['worker_teams'] = worker.teams.all()

        return context


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    fields = ["username", "first_name", "last_name", "position", "email"]

    def get_success_url(self):
        return reverse_lazy("task:worker-detail", kwargs={"pk": self.object.pk})


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task:index")

    def delete(self, request, *args, **kwargs):
        user = self.get_object()  # Get the worker being deleted
        if user == request.user:  # Ensure the logged-in user is deleting themselves
            logout(request)  # Log out the user
        return super().delete(request, *args, **kwargs)
