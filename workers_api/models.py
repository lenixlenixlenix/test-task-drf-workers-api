# Status ->  Ожидает исполнителя, В процессе, Выполнена. 
# Client -> ForeignKey
# Employee -> ForeignKey
# Date of creation
# Date of update
# Date of closing(if set cannot modify)
# Report
# ```

from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


from accounts.models import CustomUser

STATUSES = (
    ("Waiting for employee", "Waiting for employee"),
    ("In progress", "In progress"),
    ("Completed", "Completed"),
)

class Task(models.Model):
    name = models.CharField(max_length=50)
    client = models.ForeignKey(CustomUser, related_name="client_tasks" , on_delete=models.CASCADE, limit_choices_to={'is_client': True})
    employee = models.ForeignKey(CustomUser, null=True, related_name='employee_task',blank=True, on_delete=models.CASCADE, limit_choices_to={'is_employee': True})
    status = models.CharField(max_length=30, choices=STATUSES)
    date_creation = models.DateTimeField(auto_created=True, auto_now_add=True, blank=False)
    date_update = models.DateTimeField(auto_now_add=True, blank=True)
    date_closed = models.DateTimeField(blank=True, null=True)
    report = models.TextField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.name + "-" + self.client.username

    def save(self, *args, **kwargs):
        if self.status == "Completed" and not self.date_closed:
            self.date_closed = datetime.now()
            if len(self.report) < 10:
                return ValidationError("Report cannot be empty or less than 10 chars", code=401)

        super().save(*args, **kwargs)
