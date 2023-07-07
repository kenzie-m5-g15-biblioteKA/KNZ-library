from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Lending, LendingStatusChoice
from .permissions import (
    CollaboratorOrOwnerPermission,
    CollaboratorPermission,
    IsNotBlocked,
    SelfPermission,
)
from .serializers import LendingSerializer


class LendingCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsNotBlocked]

    queryset = Lending.objects.all()
    serializer_class = LendingSerializer

    def perform_create(self, serializer: LendingSerializer):
        copy_id = self.kwargs.get(self.lookup_field)
        return_date = serializer.instance.get_return_date()

        serializer.save(
            copy_id=copy_id, return_date=return_date, user=self.request.user
        )


class LendingHistoryView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CollaboratorPermission]

    queryset = Lending.objects.all()
    serializer_class = LendingSerializer


class LendingHistoryByUserView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CollaboratorOrOwnerPermission]

    lookup_url_kwarg = "user_id"
    serializer_class = LendingSerializer

    def get_queryset(self):
        kwarg_key = self.lookup_url_kwarg
        user_id = self.kwargs.get(kwarg_key)

        return Lending.objects.filter(user_id=user_id)


class LendingReturnView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, SelfPermission]

    serializer_class = LendingSerializer

    def get_queryset(self):
        kwarg_key = self.lookup_url_kwarg
        lending_id = self.kwargs.get(kwarg_key)

        return Lending.objects.filter(pk=lending_id)

    def perform_update(self, serializer):
        kwarg_key = self.lookup_url_kwarg
        lending_id = self.kwargs.get(kwarg_key)
        instance = get_object_or_404(Lending, pḱ=lending_id)

        self.check_object_permissions(self.request, instance)
        instance.get_return_book()
        instance.get_status()
        instance.save()


class LendingCheckOverdueView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CollaboratorPermission]

    queryset = Lending.objects.filter(status=LendingStatusChoice.LENT)
    serializer_class = LendingSerializer

    def update_overdue_lendings(self, lendings):
        today = now().date()

        for lending in lendings:
            if lending.return_date > today:
                lending.status = LendingStatusChoice.OVERDUE
                lending.save(update_fields=["status"])

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        self.update_overdue_lendings(queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)
