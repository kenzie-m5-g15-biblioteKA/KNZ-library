from rest_framework import generics
from django.shortcuts import get_object_or_404
from books.models import Book
from .models import Copy
from .serializers import CopySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import IsStaff, IsStaffOrSafeMethods
from drf_spectacular.utils import extend_schema


class CopyView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    @extend_schema(
        operation_id="Copies_GET",
        description="Rota de listagem de copias, retornando todas as copias cadastrados no sistema. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Listagem de copias",
        tags=["Copies"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CreateCopyView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer
    lookup_url_kwarg = "pk"

    @extend_schema(
        operation_id="Copies_POST",
        description="Rota de criação de copias, retornando a copia criada e adicionando-a no banco de dados. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Criação de Copias",
        tags=["Copies"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        self.check_object_permissions(self.request, self.request.user)
        book = get_object_or_404(Book, pk=self.kwargs.get("pk"))
        serializer.save(book=book)


class CopyDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffOrSafeMethods]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    @extend_schema(
        operation_id="Copies_GET (ID da Copia)",
        description="Rota de listagem da copia, retornando a copia cadastrado no sistema com o mesmo ID passado na URL. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Listagem de uma Copia Específica (ID da Copia)",
        tags=["Copies"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="Copies_PUT (ID da Copia)",
        description="Rota de atualização da copia, retornando a copia atualizada no sistema com o mesmo ID passado na URL. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Atualização de uma Copia Específica (ID da Copia)",
        tags=["Copies"],
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        operation_id="Copies_PUT (ID da Copia)",
        description="Rota de atualização da copia, retornando a copia atualizada no sistema com o mesmo ID passado na URL. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Atualização de uma Copia Específica (ID da Copia)",
        tags=["Copies"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        operation_id="Copies_DELETE (ID da Copia)",
        description="Rota de deleção da copia com o mesmo ID passado na URL, não retornando nada ao usuário. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Deleção de uma Copia Específica (ID da Copia)",
        tags=["Copies"],
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
