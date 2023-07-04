from rest_framework import generics, permissions, views


class CollaboratorOrOwnerPermission(permissions.IsAuthenticated):
    def has_permission(self, request: views.Request, view: generics.ListAPIView):
        user_id: int = view.kwargs.get(view.lookup_url_kwarg)

        if request.user.role == "student":
            return request.user.role == "staff" or request.user.id == user_id

        return request.user.id == user_id


class CollaboratorPermission(permissions.IsAuthenticated):
    def has_permission(self, request: views.Request, view: generics.ListAPIView):
        return request.user.role == "staff"
