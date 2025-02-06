from django.urls import path

from .views import (
    index,
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectDeleteView,
    ProjectUpdateView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TeamListView,
    TeamDetailView,
    TeamCreateView,
    TeamUpdateView,
    TeamDeleteView,
    WorkerDetailView,
    WorkerUpdateView,
    WorkerDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "projecs/",
        ProjectListView.as_view(),
        name="project-list",
    ),
    path("projecs/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path(
        "projecs/create/",
        ProjectCreateView.as_view(),
        name="project-create",
    ),
    path(
        "projecs/<int:pk>/update/",
        ProjectUpdateView.as_view(),
        name="project-update",
    ),
    path(
        "projecs/<int:pk>/delete/",
        ProjectDeleteView.as_view(),
        name="project-delete",
    ),
    path("projects/<int:pk>/task/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path(
        "teams/",
        TeamListView.as_view(),
        name="team-list",
    ),
    path("teams/<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
    path(
        "teams/create/",
        TeamCreateView.as_view(),
        name="team-create",
    ),
    path(
        "teams/<int:pk>/update/",
        TeamUpdateView.as_view(),
        name="team-update",
    ),
    path(
        "teams/<int:pk>/delete/",
        TeamDeleteView.as_view(),
        name="team-delete",
    ),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path(
        "workers/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update",
    ),
    path(
        "workers/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker-delete",
    ),
]

app_name = "task"
