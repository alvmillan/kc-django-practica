from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):

    def has_permission(self, request, view):

        if view.action == 'create' or request.user.is_superuser:
            return True

        return request.user.is_authenticated and view.action in ['retrieve', 'update', 'destroy']

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user == obj