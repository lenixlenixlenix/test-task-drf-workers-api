from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_employee and request.user.groups.filter(name="Employee")

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True


class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_client and request.user.groups.filter(name="Client")

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return obj.client == request.user

class IsEmployeersTask(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_employee and request.user.groups.filter(name="Employee")

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'UPDATE']:
            return obj.employee == request.user or obj.status == "Waiting for employee"
         