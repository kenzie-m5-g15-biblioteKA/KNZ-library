from rest_framework import generics
from .models import Book
from django.shortcuts import get_object_or_404
from users.serializers import UserSerializer
from .serializers import BookSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from users.permissions import IsStaff, IsStaffOrSafeMethods


class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        self.check_object_permissions(self.request, self.request.user)
        serializer.save()


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffOrSafeMethods]

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookFollowView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_url_kwarg = "pk"

    def perform_update(self, serializer):
        self.check_object_permissions(self.request, self.request.user)
        pk = self.kwargs.get("pk")

        book = get_object_or_404(Book, pk=pk)
        book = BookSerializer(instance=book)

        user = self.request.user
        user = UserSerializer(instance=user)

        aux = True
        response = []

        for item in book.data["followers"]:
            response.append(item["id"])

        for item in response:
            if user.data["id"] == item:
                aux = False

        if aux == True:
            response.append(user.data["id"])

        serializer.save(followers=response)


class BookUnfollowView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_url_kwarg = "pk"

    def perform_update(self, serializer):
        self.check_object_permissions(self.request, self.request.user)
        pk = self.kwargs.get("pk")

        book = get_object_or_404(Book, pk=pk)
        book = BookSerializer(instance=book)

        user = self.request.user
        user = UserSerializer(instance=user)

        aux = False
        response = []

        for item in book.data["followers"]:
            response.append(item["id"])

        for item in response:
            if user.data["id"] == item:
                aux = True

        if aux:
            for item in response:
                if item == user.data["id"]:
                    response.remove(item)

            serializer.save(followers=response)
