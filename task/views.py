from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TaskForm
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
        task = get_object_or_404(Task, pk=self.kwargs["pk"])  # Get the Task
        kwargs["project"] = task.project  # Pass its Project to the form
        return kwargs

    def get_success_url(self):
        return reverse_lazy("task:project-detail", kwargs={"pk": self.object.project.pk})


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
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("task:team-detail", kwargs={"pk": self.object.pk})


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("task:team-detail", kwargs={"pk": self.object.pk})


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("task:team-list")
