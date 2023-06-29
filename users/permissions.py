from rest_framework import permissions
from .models import User
from rest_framework.views import View


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: User) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and obj == request.user


class IsCollaborator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            user = User.objects.get(username=request.user)
        except:
            return False

        if user.type_user == "Collaborator":
            return True

        return False
