from rest_framework import permissions


class PostPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return view.action == 'retrieve' or request.user.is_superuser or request.user == obj.published_on.owner
