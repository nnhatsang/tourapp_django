from rest_framework import permissions


class OwnerPermisson(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.user and request.user)

class UserOwnerPermisson(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user == obj)

