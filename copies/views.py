from rest_framework import generics
from django.shortcuts import get_object_or_404
from books.models import Book
from .models import Copy
from .serializers import CopySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import IsStaff, IsStaffOrSafeMethods


class CopyView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer


class CreateCopyView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer
    lookup_url_kwarg = "pk"

    def perform_create(self, serializer):
        self.check_object_permissions(self.request, self.request.user)
        book = get_object_or_404(Book, pk=self.kwargs.get("pk"))
        serializer.save(book=book)


class CopyDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffOrSafeMethods]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer
