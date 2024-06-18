from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import CustomUser
from workers_api.models import Task

class Command(BaseCommand):
    help = "Initialization of groups for client and employee"

    def handle(self, *args, **kwargs):
        client_group, created = Group.objects.get_or_create(name="Client")
        employee_group, created = Group.objects.get_or_create(name="Employee")

        task_content_type = ContentType.objects.get_for_model(Task)

        # client_permissions = [
        #     Permission.objects.get_or_create(codename="task.add_task", content_type=task_content_type),
        #     Permission.objects.get_or_create(codename="task.view_task", content_type=task_content_type),
        # ]

        # employee_permissions = [
        #     Permission.objects.get_or_create(codename="task.view_task", content_type=task_content_type),
        #     Permission.objects.get_or_create(codename="task.set_task", content_type=task_content_type),
        # ]
        # client_group.permissions.set(client_permissions)
        # employee_group.permissions.set(employee_permissions)

        self.stdout.write(self.style.SUCCESS('Successfully created groups and assigned permissions'))

