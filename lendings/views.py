from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from books.models import AvailabilityOptions, Book
from books.serializers import BookSerializer
from copies.models import Copy
from copies.serializers import CopySerializer

from .models import Lending, LendingStatusChoice
from .permissions import (
    CollaboratorOrOwnerPermission,
    CollaboratorPermission,
    IsNotBlocked,
    SelfPermission,
)
from .serializers import LendingSerializer


class LendingCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsNotBlocked]

    queryset = Lending.objects.all()
    serializer_class = LendingSerializer

    @extend_schema(
        operation_id="Lending_POST (ID da Copia)",
        description="Rota de criação de empréstimos, retornando a empréstimo criada e adicionando-a no banco de dados. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Criação de Empréstimos",
        tags=["Lendings"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs) -> Response:
        copy_id = self.kwargs.get(self.lookup_field)
        copy = get_object_or_404(Copy, pk=copy_id)
        book = get_object_or_404(Book, pk=copy.book.pk)

        if book and book.availability == AvailabilityOptions.UNAVAILABLE:
            return Response(
                {
                    "Message": "Este livro não está disponível para empréstimo no momento"
                },
                status.HTTP_400_BAD_REQUEST,
            )

        user_lending = Lending.objects.filter(
            status=LendingStatusChoice.LENT | LendingStatusChoice.OVERDUE,
            user=self.request.user,
            copy=copy,
        )
        if user_lending:
            return Response(
                {"message": "Você possui um empréstimo em aberto para esse livro"},
                status=status.HTTP_409_CONFLICT,
            )

        copy.copies -= 1
        copy.save()
        if copy.copies < 1:
            book.availability = AvailabilityOptions.UNAVAILABLE
            book.save()

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer: LendingSerializer):
        copy_id = self.kwargs.get(self.lookup_field)
        copy = get_object_or_404(Copy, pk=copy_id)

        return_date = serializer.instance.get_return_date()

        serializer.save(copy=copy, return_date=return_date, user=self.request.user)


class LendingHistoryView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CollaboratorPermission]

    queryset = Lending.objects.all()
    serializer_class = LendingSerializer

    @extend_schema(
        operation_id="Lending_GET",
        description="Rota de listagem de empréstimos, retornando todos os empréstimos cadastrados no sistema.  É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Listagem de Empréstimos",
        tags=["Lendings"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LendingDetailView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CollaboratorPermission]

    lookup_url_kwarg = "lending_id"
    serializer_class = LendingSerializer

    def get_queryset(self):
        kwarg_key = self.lookup_url_kwarg
        lending_id = self.kwargs.get(kwarg_key)

        return Lending.objects.filter(pk=lending_id)

    @extend_schema(
        operation_id="Lending_GET (ID do Empréstimo)",
        description="Rota de listagem de empréstimo, retornando o empréstimo cadastrado no sistema com o mesmo ID passado na URL. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Listagem de um Empréstimo Específico (ID do Empréstimo)",
        tags=["Lendings"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class LendingHistoryByUserView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CollaboratorOrOwnerPermission]

    lookup_url_kwarg = "user_id"
    serializer_class = LendingSerializer

    def get_queryset(self):
        kwarg_key = self.lookup_url_kwarg
        user_id = self.kwargs.get(kwarg_key)

        return Lending.objects.filter(user_id=user_id)

    @extend_schema(
        operation_id="Lending_GET (ID do Empréstimo)",
        description="Rota de listagem de empréstimo por usuário, retornando a lista de empréstimos feitos pelo usuário buscado. É necessário estar autenticado e ser dono do perfil ou colaborador para acessar essa rota",
        summary="Listagem de empréstimos por usuário",
        tags=["Lendings"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LendingReturnView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, SelfPermission]

    lookup_url_kwarg = "lending_id"
    serializer_class = LendingSerializer

    def get_queryset(self):
        kwarg_key = self.lookup_url_kwarg
        lending_id = self.kwargs.get(kwarg_key)

        return Lending.objects.filter(pk=lending_id)

    @extend_schema(
        operation_id="Lending_PATCH (ID do Empréstimo)",
        description="Rota de atualização parcial do empréstimo, retornando o empréstimo atualizado no sistema com o mesmo ID passado na URL. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Atualização parcial de um Empréstimo Específico (ID do Empréstimo)",
        tags=["Lendings"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def update(self, request, *args, **kwargs) -> Response:
        kwarg_key = self.lookup_url_kwarg
        lending_id = self.kwargs.get(kwarg_key)
        lending_obj = get_object_or_404(Lending, pk=lending_id)

        copy_obj = get_object_or_404(Copy, pk=lending_obj.copy.pk)
        book_obj = get_object_or_404(Book, pk=copy_obj.book.pk)

        if copy_obj:
            copy_obj.copies += 1
            copy_obj.save()

        if book_obj and book_obj.availability == AvailabilityOptions.UNAVAILABLE:
            book_obj.availability = AvailabilityOptions.AVAILABLE
            book_obj.save()

        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        kwarg_key = self.lookup_url_kwarg
        lending_id = self.kwargs.get(kwarg_key)
        lending_obj = get_object_or_404(Lending, pk=lending_id)

        self.check_object_permissions(self.request, lending_obj)
        lending_obj.get_return_book()
        lending_obj.get_status()
        lending_obj.save()


class LendingCheckOverdueView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CollaboratorPermission]

    queryset = Lending.objects.all()
    serializer_class = LendingSerializer

    def update_overdue_lendings(self, lendings):
        today = now().date()

        for lending in lendings:
            if lending.return_date > today:
                lending.status = LendingStatusChoice.OVERDUE
                lending.save(update_fields=["status"])

    @extend_schema(exclude=True)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(status=LendingStatusChoice.LENT)
        self.update_overdue_lendings(queryset)

        return super().list(request, *args, **kwargs)
