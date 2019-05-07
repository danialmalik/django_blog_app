from rest_framework import permissions


class IsPostOwner(permissions.BasePermission):
    """Permission to only allow users to get and update their own Post."""

    def has_object_permission(self, request, view, obj):
        return obj.posted_by == request.user


class IsCommentOwner(permissions.BasePermission):
    """Permission to only allow users to get and update their own Comment."""

    def has_object_permission(self, request, view, obj):
        return obj.commented_by == request.user
