from django import forms
from django.contrib.auth import get_user_model
from .models import Task, Project

User = get_user_model()

class TaskForm(forms.ModelForm):
    deadline = forms.DateField(
        widget=forms.SelectDateWidget(),  # Mini calendar dropdown for Year, Month, Day
        required=True
    )

    assignees = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),  # Empty initially, will be set in __init__
        widget=forms.CheckboxSelectMultiple,
        label="Assignees (Position)"
    )

    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "is_completed", "priority", "task_type", "assignees"]

    def __init__(self, *args, **kwargs):
        project = kwargs.pop("project", None)  # Get the project instance from the view
        super().__init__(*args, **kwargs)

        if project:
            self.fields["assignees"].queryset = User.objects.filter(teams__in=project.teams.all())
 # Filter by project team

            # Modify the display labels to show user name + position
            self.fields["assignees"].label_from_instance = lambda user: f"{user.first_name} {user.last_name} ({user.position.name})"
