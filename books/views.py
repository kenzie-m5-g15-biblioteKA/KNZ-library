from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.permissions import IsStaff, IsStaffOrSafeMethods
from users.serializers import UserSerializer

from .models import Book
from .serializers import BookSerializer


class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @extend_schema(
        operation_id="Books_GET",
        description="Rota de listagem de livros, retornando todos os livros cadastrados no sistema. Não é necessário autenticação",
        summary="Listagem de Livros",
        tags=["Books"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        operation_id="Books_POST",
        description="Rota de criação de livros, retornando o livro criado e adicionando-o no banco de dados. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Criação de Livros",
        tags=["Books"],
    )
    def post(self, request, *args, **kwargs):
        self.check_object_permissions(self.request, self.request.user)
        return self.create(request, *args, **kwargs)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffOrSafeMethods]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @extend_schema(
        operation_id="Books_GET (ID do Livro)",
        description="Rota de listagem do livro, retornando o livro cadastrado no sistema com o mesmo ID passado na URL. Não é necessário autenticação",
        summary="Listagem de um Livro Específico (ID do Livro)",
        tags=["Books"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="Books_PUT (ID do Livro)",
        description="Rota de atualização do livro, retornando o livro atualizado no sistema com o mesmo ID passado na URL. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Atualização de um Livro Específico (ID do Livro)",
        tags=["Books"],
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        operation_id="Books_PUT (ID do Livro)",
        description="Rota de atualização do livro, retornando o livro atualizado no sistema com o mesmo ID passado na URL. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Atualização de um Livro Específico (ID do Livro)",
        tags=["Books"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        operation_id="Books_DELETE (ID do Livro)",
        description="Rota de deleção do livro com o mesmo ID passado na URL, não retornando nada ao usuário. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Deleção de um Livro Específico (ID do Livro)",
        tags=["Books"],
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BookFollowView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_url_kwarg = "pk"

    @extend_schema(
        operation_id="Books_PUT (ID do Livro)",
        description="Rota para seguir um livro com o mesmo ID passado na URL, retornando o livro seguido. É necessário estar autenticado para acessar essa rota",
        summary="Segue um Livro Específico (ID do Livro)",
        tags=["Books"],
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        operation_id="Books_PUT (ID do Livro)",
        description="Rota para deixar de seguir um livo com o mesmo ID passado na URL, retornando o livro não mais seguido. É necessário estar autenticado para acessar essa rota",
        summary="Deixa de Segue um Livro Específico (ID do Livro)",
        tags=["Books"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

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

    @extend_schema(
        operation_id="Books_PUT (ID do Livro)",
        description="Rota para deixar de seguir um livo com o mesmo ID passado na URL, retornando o livro não mais seguido. É necessário estar autenticado para acessar essa rota",
        summary="Deixa de Segue um Livro Específico (ID do Livro)",
        tags=["Books"],
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        operation_id="Books_PUT (ID do Livro)",
        description="Rota para deixar de seguir um livo com o mesmo ID passado na URL, retornando o livro não mais seguido. É necessário estar autenticado para acessar essa rota",
        summary="Deixa de Segue um Livro Específico (ID do Livro)",
        tags=["Books"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        operation_id="Books_PUT (ID do Livro)",
        description="Rota para deixar de seguir um livo com o mesmo ID passado na URL, retornando o livro não mais seguido. É necessário estar autenticado para acessar essa rota",
        summary="Deixa de Segue um Livro Específico (ID do Livro)",
        tags=["Books"],
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        operation_id="Books_PUT (ID do Livro)",
        description="Rota para deixar de seguir um livo com o mesmo ID passado na URL, retornando o livro não mais seguido. É necessário estar autenticado para acessar essa rota",
        summary="Deixa de Segue um Livro Específico (ID do Livro)",
        tags=["Books"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        operation_id="Books_PUT (ID do Livro)",
        description="Rota para deixar de seguir um livo com o mesmo ID passado na URL, retornando o livro não mais seguido. É necessário estar autenticado para acessar essa rota",
        summary="Deixa de Segue um Livro Específico (ID do Livro)",
        tags=["Books"],
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

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
