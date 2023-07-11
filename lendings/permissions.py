from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.views import Request

from lendings.models import Lending
from users.models import User, UserStatusChoice


class CollaboratorOrOwnerPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: ListAPIView) -> bool:
        user_id: int = view.kwargs.get(view.lookup_url_kwarg)
        searched_user = get_object_or_404(User, pk=user_id)

        if searched_user.role == "student":
            return request.user.role == "staff" or request.user == searched_user

        return request.user == searched_user


class CollaboratorPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        return request.user.role == "staff"


class SelfPermission(permissions.BasePermission):
    def has_object_permission(self, request: Request, view, obj: Lending) -> bool:
        return obj.user == request.user


class IsNotBlocked(permissions.BasePermission):
    def has_permission(self, request: Request, view):
        return request.user.status == UserStatusChoice.ACTIVE
