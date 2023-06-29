from django.shortcuts import get_object_or_404
from rest_framework import generics
from users.models import User
from .models import Books
from .serializers import BooksSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from users.permissions import IsCollaborator


class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCollaborator]

    queryset = Books.objects.all()
    serializer_class = BooksSerializer

    def perform_create(self, serializer):
        self.check_object_permissions(self.request, self.request.user)
        serializer.save()


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Books.objects.all()
    serializer_class = BooksSerializer
