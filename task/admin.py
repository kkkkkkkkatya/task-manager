from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from task.models import Worker, Project, Position, TaskType, Task, Team


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                    )
                },
            ),
        )
    )


admin.site.register(Project)

admin.site.register(TaskType)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ("project__name",)
    list_filter = ("priority", "is_completed", "deadline", "task_type__name")


admin.site.register(Team)

admin.site.register(Position)
