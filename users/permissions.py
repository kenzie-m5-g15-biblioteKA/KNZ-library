from rest_framework import permissions

from .models import User


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: User) -> bool:
        return request.user.is_authenticated and obj == request.user


class IsStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            user = User.objects.get(username=request.user)
        except:
            return False

        if user.role == "staff":
            return True

        return False


class IsStaffOrSafeMethods(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            user = User.objects.get(username=request.user)
        except:
            return False

        if user.role == "staff":
            return True

        return False
