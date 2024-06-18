from django.contrib.auth.models import Group
from accounts.models import CustomUser

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, views, status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import CustomUserSerializer, TaskSerializer, EditTaskForEmployeeSerizalizer
from .permissions import IsClient, IsEmployee, IsEmployeersTask


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head']

    def perform_create(self, serializer):
        data = serializer.validated_data

        if data['is_client'] is not None and data['is_employee'] is not None:
            raise ValidationError("User can be only client or employee", code=401) 


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def retrieve(self, request, pk=None):
        user = self.request.user
        queryset = Task.objects.filter(employee=user)
        task = get_object_or_404(queryset, pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def list(self, request):
        user = self.request.user
        if user.is_client:
            serializer =  TaskSerializer(Task.objects.filter(client=user), many=True)
            return Response(serializer.data)
        elif user.is_employee and not user.has_perm('workers_api.view_all_tasks'):
            # list tasks that are not with employee and employee is current user
            q1= Task.objects.filter(status="Waiting for employee")
            q2 = Task.objects.filter(employee=user)
            serializer = TaskSerializer(q1.union(q2), many=True)
            return Response(serializer.data)
        else:
            serializer = TaskSerializer(Task.objects.all(), many=True)
            return Response(serializer.data)

    def perform_create(self, serializer):
        data = serializer.validated_data

        if data['status'] != 'Waiting for employee' and data['employee'] is None:
            raise ValidationError("Task cannot have employee with status waiting", code=401) 
        if data['status'] == 'Completed' and data['report'] == "":
            raise ValidationError("Completed task must have a report", code=401) 

        serializer.save()
    def perform_updates(self, serializer):
        data = serializer.validated_data

        if data['status'] == 'Completed' and data['report'] == "":
            raise ValidationError("Completed task must have a report", code=401) 

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsClient]
        if self.action in ['update', 'partial_update']:
            # only clients can create tasks, employee can update if it his task
            if self.request.user.groups.filter(name='Client').exists():
                self.permission_classes = [IsClient]
            elif self.request.user.groups.filter(name='Employee').exists():
                self.permission_classes = [IsEmployee]

        elif self.action in ['list', 'retrive']:
            if self.request.user.groups.filter(name='Employee').exists():
                self.permission_classes = [IsEmployee]
            else:
                self.permission_classes = [IsClient]
        return super(TaskViewSet, self).get_permissions()
    
class CurrentUserView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = self.request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

class EditTaskEmployee(generics.UpdateAPIView):
    permission_classes = [IsEmployeersTask]
    queryset = Task.objects.all()
    serializer_class = EditTaskForEmployeeSerizalizer

    def get(self, request, pk):
        obj= self.queryset.get(pk=pk)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)



