from rest_framework import serializers

from accounts.models import CustomUser

from .models import Task

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone", "is_client", "is_employee"]

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id","name", "client", "employee", "status", "date_creation", "date_update", "date_closed", "report"]

        
class EditTaskForEmployeeSerizalizer(serializers.ModelSerializer):    
    class Meta:
        model = Task
        fields = ["name", "client", "status", "employee", "date_creation", "date_update", "date_closed", "report"]
        read_only_fields = ["name","date_creation",'date_update',"client"] 




