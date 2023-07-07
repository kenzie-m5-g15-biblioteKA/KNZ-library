from lending.serializers import LendingsSerializer
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from lending.models import Lending
from .serializers import UserSerializer, UserStatusSerializer
from .permissions import IsAccountOwner, IsStaff
from rest_framework import generics
from drf_spectacular.utils import extend_schema


class UserView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff]

    queryset = User.objects.all()
    serializer_class = UserStatusSerializer
    user = "user"

    @extend_schema(
        operation_id="Users_get",
        description="rota de listagem de usuarios",
        summary="listagem de usuaroius",
        tags=["user"],
    )
    def get(self, request, *args, **kwargs):
        self.check_object_permissions(request, request.user)
        return self.list(request, *args, **kwargs)


class UserLendingView(generics.RetrieveAPIView):
    queryset = Lending.objects.all()
    serializer_class = LendingsSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff | IsAccountOwner]


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff]
