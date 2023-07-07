from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.views import Request

from lendings.models import Lending
from users.models import User


class CollaboratorOrOwnerPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: ListAPIView) -> bool:
        user_id: int = view.kwargs.get(view.lookup_url_kwarg)
        searched_user = get_object_or_404(User, pk=user_id)
        searched_user_role: bool = searched_user.role

        if searched_user_role == "student":
            return request.user.role == "staff" or request.user == searched_user

        return request.user == searched_user


class CollaboratorPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: ListAPIView) -> bool:
        return request.user.role == "staff"


class SelfPermission(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: UpdateAPIView, obj: Lending
    ) -> bool:
        return obj.user == request.user
