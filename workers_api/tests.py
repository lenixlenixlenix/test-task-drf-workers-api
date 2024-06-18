from django.test import TestCase
from time import time
from .models import Task

from accounts.models import CustomUser
# Create your tests here.

class TaskTests(TestCase):
    def setUp(self):
        user_client = CustomUser.create(email="email@email.com", password="secret42-69777", username="notleonid", is_client=True)
        user_employee = CustomUser.create(email="email@email.com", password="secret42-69777", username="maybeleonid", is_employee=True)

        Task.objects.create(name="Do a backflip", client=user_client, employee=user_employee, status="In progress")
        