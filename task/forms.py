from django import forms
from django.contrib.auth import get_user_model
from .models import Task, Project, Team

User = get_user_model()

### form for task
class TaskForm(forms.ModelForm):
    #change deadline widget
    deadline = forms.DateField(
        widget=forms.SelectDateWidget(),
        required=True
    )

    #change assignees widget
    assignees = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label="Assignees (Position)"
    )

    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "is_completed", "priority", "task_type", "assignees"]

    def __init__(self, *args, **kwargs):
        project = kwargs.pop("project", None)
        super().__init__(*args, **kwargs)

        if project:
            self.fields["assignees"].queryset = User.objects.filter(teams__in=project.teams.all()) #gives only team members

            self.fields["assignees"].label_from_instance = lambda user: f"{user.first_name} {user.last_name} ({user.position.name})"


### form for team
class TeamForm(forms.ModelForm):

    #change members widget
    members = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),  # Empty initially, will be set in __init__
        widget=forms.CheckboxSelectMultiple,
        label="Members (Position)"
    )

    class Meta:
        model = Team
        fields = "__all__"
