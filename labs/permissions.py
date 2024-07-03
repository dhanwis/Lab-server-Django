from rest_framework.permissions import BasePermission

class IsLab(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_lab


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_customer
    


class IsAdminAndLab(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff and request.user.is_lab
