from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import Permission

from django.contrib.contenttypes.models import ContentType

class CustomUser(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    phone = models.IntegerField(default=375)

    # can be changed to CharField(choices)
    def save(self, *args, **kwargs):
        if self.is_client and self.is_employee:
            return ValueError("User cannot be both client and employee")
        super().save(*args, **kwargs)

        

