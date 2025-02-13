# Generated by Django 5.1.5 on 2025-02-03 17:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task", "0002_task_assignees"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="assignees",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="tasks", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
