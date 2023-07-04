from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Lending
from .permissions import CollaboratorOrOwnerPermission, CollaboratorPermission
from .serializers import LendingSerializer


class LendingCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
    permission_classes = [CollaboratorPermission]

    queryset = Lending.objects.all()
    serializer_class = LendingSerializer


class LendingHistoryByUserView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CollaboratorOrOwnerPermission]

    lookup_url_kwarg = "user_id"
    serializer_class = LendingSerializer

    def get_queryset(self):
        return Lending.objects.filter(user_id=self.kwargs.get(self.lookup_url_kwarg))
