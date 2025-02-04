from django.urls import path

from .views import index, ProjectListView, ProjectDetailView

urlpatterns = [
    path("", index, name="index"),
    path(
        "projecs/",
        ProjectListView.as_view(),
        name="project-list",
    ),
    path("projecs/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),

]

app_name = "task"
