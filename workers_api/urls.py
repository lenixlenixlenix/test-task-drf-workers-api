from django.urls import path, include
from .views import CustomUserViewSet, TaskViewSet, CurrentUserView, EditTaskEmployee

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/currentuser",CurrentUserView.as_view(), name="current-user" ),
    path("api/<int:pk>/employee_task", EditTaskEmployee.as_view(), name="employee-edit"),
]