from rest_framework import generics
from books.models import Book
from books.serializers import BookSerializer
from .models import Assessments
from django.shortcuts import get_object_or_404
from .serializers import AssessmentsSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsStaff
from drf_spectacular.utils import extend_schema


class CreateAssessmentsView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Assessments.objects.all()
    serializer_class = AssessmentsSerializer

    @extend_schema(
        operation_id="Assessments_POST",
        description="Rota de criação de avaliações, retornando a avaliação criada e adicionando-a no banco de dados. É necessário estar autenticado acessar essa rota",
        summary="Criação de Avaliações",
        tags=["Assessments"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

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

    @extend_schema(
        operation_id="Assessments_GET",
        description="Rota de listagem de avaliações, retornando todas as avaliações cadastrados no sistema. É necessário estar autenticado para acessar essa rota",
        summary="Listagem de Avaliações",
        tags=["Assessments"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AssessmentsDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff]

    queryset = Assessments.objects.all()
    serializer_class = AssessmentsSerializer

    @extend_schema(
        operation_id="Assessments_GET (ID da Avaliação)",
        description="Rota de listagem da Avaliação, retornando a Avaliação cadastrado no sistema com o mesmo ID passado na URL. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Listagem de uma Avaliação Específica (ID da Avaliação)",
        tags=["Assessments"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="Assessments_PUT (ID da Avaliação)",
        description="Rota de atualização da Avaliação, retornando a Avaliação atualizada no sistema com o mesmo ID passado na URL. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Atualização de uma Avaliação Específica (ID da Avaliação)",
        tags=["Assessments"],
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        operation_id="Assessments_PUT (ID da Avaliação)",
        description="Rota de atualização da Avaliação, retornando a Avaliação atualizada no sistema com o mesmo ID passado na URL. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Atualização de uma Avaliação Específica (ID da Avaliação)",
        tags=["Assessments"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        operation_id="Assessments_DELETE (ID da Avaliação)",
        description="Rota de deleção da Avaliação com o mesmo ID passado na URL, não retornando nada ao usuário. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Deleção de uma Avaliação Específica (ID da Avaliação)",
        tags=["Assessments"],
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

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
