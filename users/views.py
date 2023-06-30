from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from .serializers import UserSerializer
from .permissions import IsAccountOwner, IsStaff
from rest_framework import generics


# class UserView(generics.ListCreateAPIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsStaff]

#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def list(self, request, *args, **kwargs):
#         self.check_object_permissions(request, request.user)
#         queryset = self.filter_queryset(self.get_queryset())

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)


"""Teste"""


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLendingView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
