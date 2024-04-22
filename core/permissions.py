from rest_framework.permissions import BasePermission

from UserManagement.models import AdminModel


class IsSuperAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.admin.role == 'super_admin' if hasattr(request.user, 'admin') else False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'admin')


class IsAdminOrSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return hasattr(request.user, 'admin') or obj == request.user
