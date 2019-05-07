from rest_framework import permissions


class IsSelf(permissions.BasePermission):
    """Permission to only allow users to get and update their own data."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
