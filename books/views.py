from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import User
from users.permissions import IsStaff

from .models import Book
from .serializers import BooksSerializer


class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff]

    queryset = Book.objects.all()
    serializer_class = BooksSerializer

    def perform_create(self, serializer):
        self.check_object_permissions(self.request, self.request.user)
        serializer.save()


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BooksSerializer
