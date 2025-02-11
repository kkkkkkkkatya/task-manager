from django.contrib.auth import get_user_model
from django.test import TestCase
from task.models import Project, TaskType, Task, Team, Position


class ModelsTests(TestCase):
    def test_project_str(self):
        project = Project.objects.create(
            name="Project Alpha",
            description="A test project"
        )
        self.assertEqual(str(project), project.name)

    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="Bug Fix")
        self.assertEqual(str(task_type), task_type.name)

    def test_task_str(self):
        project = Project.objects.create(
            name="Project Beta",
            description="Another test project"
        )
        task_type = TaskType.objects.create(name="Feature")
        task = Task.objects.create(
            name="Implement Login",
            description="Implement authentication system",
            deadline="2025-12-31",
            priority="High",
            task_type=task_type,
            project=project
        )
        self.assertEqual(str(task), f"{task.name} related to {project.name}, deadline: {task.deadline}")

    def test_team_str(self):
        project = Project.objects.create(
            name="Project Gamma",
            description="Team test project"
        )
        team = Team.objects.create(name="Development Team", project=project)
        self.assertEqual(str(team), team.name)

    def test_position_str(self):
        position = Position.objects.create(name="Software Engineer")
        self.assertEqual(str(position), position.name)

    def test_worker_str(self):
        user = get_user_model().objects.create_user(
            username="johndoe",
            password="test1234",
            first_name="John",
            last_name="Doe"
        )
        self.assertEqual(str(user), f"{user.username} ({user.first_name} {user.last_name})")
