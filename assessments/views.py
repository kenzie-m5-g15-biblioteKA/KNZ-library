from rest_framework import generics
from books.models import Book
from books.serializers import BookSerializer
from .models import Assessments
from django.shortcuts import get_object_or_404
from .serializers import AssessmentsSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsStaff


class CreateAssessmentsView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Assessments.objects.all()
    serializer_class = AssessmentsSerializer

    def perform_create(self, serializer):
        user = self.request.user
        pk = self.kwargs.get("pk")

        book = get_object_or_404(Book, pk=pk)
        book_data = BookSerializer(instance=book)
        book_data = book_data.data

        serializer.save(user=user, book=book)

        book = get_object_or_404(Book, pk=pk)
        book_data = BookSerializer(instance=book)
        book_data = book_data.data

        assessments = book_data["assessments"]
        queryset = Assessments.objects.all()
        queryset = AssessmentsSerializer(instance=queryset, many=True)
        queryset = queryset.data

        aux = 0
        stars = 0
        total = 0

        for assessment in assessments:
            for item in queryset:
                if assessment["id"] == item["id"]:
                    aux = aux + 1
                    stars = stars + item["stars"]
        total = stars / aux
        total = round(total, 2)

        validated_data = {"ranking": total}
        book_data = BookSerializer(
            instance=book,
            data=validated_data,
            partial=True,
        )
        book_data.is_valid(raise_exception=True)
        book_data.save()


class ListAssessmentsView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Assessments.objects.all()
    serializer_class = AssessmentsSerializer


class AssessmentsDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff]

    queryset = Assessments.objects.all()
    serializer_class = AssessmentsSerializer

    def perform_destroy(self, instance):
        pk = self.kwargs.get("pk")

        assessment = get_object_or_404(Assessments, pk=pk)
        instance.delete()

        book = get_object_or_404(Book, pk=assessment.book.id)
        book_data = BookSerializer(instance=book)
        book_data = book_data.data

        assessments = book_data["assessments"]
        queryset = Assessments.objects.all()
        queryset = AssessmentsSerializer(instance=queryset, many=True)
        queryset = queryset.data

        aux = 0
        stars = 0
        total = 0

        for assessment in assessments:
            for item in queryset:
                if assessment["id"] == item["id"]:
                    aux = aux + 1
                    stars = stars + item["stars"]
        total = stars / aux
        total = round(total, 2)

        validated_data = {"ranking": total}
        book_data = BookSerializer(
            instance=book,
            data=validated_data,
            partial=True,
        )
        book_data.is_valid(raise_exception=True)
        book_data.save()
