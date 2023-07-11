from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.views import Response, status
from books.models import Book
from books.serializers import BookSerializer
from copies.serializers import CopySerializer
from users.models import User
from users.serializers import UserSerializer, UserStatusSerializer
from copies.models import Copy
from .models import Lending
from .serializers import LendingsCreateSerializer, LendingsUpdateSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsStaff
from datetime import timedelta
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from django.core.mail import send_mail
from django.conf import settings


class LendingView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff]

    queryset = Lending.objects.all()
    serializer_class = LendingsCreateSerializer

    @extend_schema(
        operation_id="Lending_GET",
        description="Rota de listagem de emprestimos, retornando todos os emprestimos cadastrados no sistema.  É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Listagem de Emprestimos",
        tags=["Lending"],
    )
    def get(self, request, *args, **kwargs):
        self.check_object_permissions(request, request.user)
        return self.list(request, *args, **kwargs)


class CreateLendingView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff]

    queryset = Lending.objects.all()
    serializer_class = LendingsCreateSerializer
    lookup_url_kwarg = "pk"

    @extend_schema(
        operation_id="Lending_POST (ID da Copia)",
        description="Rota de criação de emprestimos, retornando a emprestimo criada e adicionando-a no banco de dados. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Criação de Emprestimos",
        tags=["Lending"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user = request.data["user"]
        user = get_object_or_404(User, pk=user)

        copy = get_object_or_404(Copy, pk=self.kwargs.get("pk"))
        book = get_object_or_404(Book, pk=copy.book.id)

        if user.status == "Blocked":
            return Response(
                {
                    "Message": "Este usuário esta bloqueado e imposibilitado de emprestar novos livros"
                },
                status.HTTP_400_BAD_REQUEST,
            )

        if book.availability == "unavaliable":
            return Response(
                {"Message": "Este livro não está disponivel para empréstimo"},
                status.HTTP_400_BAD_REQUEST,
            )

        if copy.copies < 1:
            validated_data = {"availability": "unavaliable"}

            book_instace = BookSerializer(
                instance=book,
                data=validated_data,
                partial=True,
            )
            book_instace.is_valid(raise_exception=True)
            book_instace.save()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        self.check_object_permissions(self.request, self.request.user)
        copy = get_object_or_404(Copy, pk=self.kwargs.get("pk"))

        book = get_object_or_404(Book, pk=copy.book.id)
        book = BookSerializer(instance=book)

        followers = len(book.data["followers"])

        validated_data = {"copies": copy.copies - 1}

        copy_instace = CopySerializer(
            instance=copy,
            data=validated_data,
            partial=True,
        )
        copy_instace.is_valid(raise_exception=True)
        copy_instace.save()

        user = self.request.data.pop("user")
        user = get_object_or_404(User, pk=user)

        created_at = timezone.now()
        return_date = created_at

        if followers <= 1:
            return_date = created_at + timedelta(days=7)

        elif followers <= 5:
            return_date = created_at + timedelta(days=5)

        else:
            return_date = created_at + timedelta(days=3)

        while return_date.weekday() >= 5:
            return_date += timedelta(days=1)

        return_date = return_date.date()

        serializer.save(user=user, copy=copy, return_date=return_date)


class LendingDetailView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Lending.objects.all()
    serializer_class = LendingsCreateSerializer

    @extend_schema(
        operation_id="Lending_GET (ID do Emprestimo)",
        description="Rota de listagem de emprestimo, retornando o emprestimo cadastrado no sistema com o mesmo ID passado na URL. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Listagem de um Emprestimo Específico (ID do Emprestimo)",
        tags=["Lending"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user = request.user
        user = UserSerializer(instance=user)

        response = []

        for item in queryset:
            item = LendingsCreateSerializer(instance=item)

            if item.data["user"]["username"] == user.data["username"]:
                response.append(item.data)
        if response == []:
            return Response(
                {"Message": "Você ainda não fez nenhum emprestimo"},
                status.HTTP_400_BAD_REQUEST,
            )

        page = self.paginate_queryset(response)

        return self.get_paginated_response(response)


class DevolutionLendingView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Lending.objects.all()
    serializer_class = LendingsCreateSerializer
    lookup_url_kwarg = "pk"

    @extend_schema(
        operation_id="Lending_PUT (ID da Emprestimo)",
        description="Rota de atualização do emprestimo, retornando o emprestimo atualizado no sistema com o mesmo ID passado na URL. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Atualização de um Emprestimo Específico (ID do Emprestimo)",
        tags=["Lending"],
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        operation_id="Lending_PUT (ID da Emprestimo)",
        description="Rota de atualização do emprestimo, retornando o emprestimo atualizado no sistema com o mesmo ID passado na URL. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Atualização de um Emprestimo Específico (ID do Emprestimo)",
        tags=["Lending"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.data["user"]
        user = get_object_or_404(User, pk=user)

        lending = get_object_or_404(Lending, pk=self.kwargs.get("pk"))

        copy = get_object_or_404(Copy, pk=lending.copy.id)
        copy_validated_data = {"copies": copy.copies + 1}

        book = get_object_or_404(Book, pk=copy.book.id)
        book_validated_data = {"availability": "avaliable"}

        copy_instace = CopySerializer(
            instance=copy,
            data=copy_validated_data,
            partial=True,
        )
        copy_instace.is_valid(raise_exception=True)
        copy_instace.save()

        book_instance = BookSerializer(
            instance=book,
            data=book_validated_data,
            partial=True,
        )
        book_instance.is_valid(raise_exception=True)
        book_instance.save()

        if lending.returned_date != None:
            return Response(
                {
                    "Message": "você não pode devolver livros que você já tenha devolvido"
                },
                status.HTTP_400_BAD_REQUEST,
            )

        if user.id != lending.user.id:
            return Response(
                {
                    "Message": "você só pode devolver livros que você tenha pego emprestado"
                },
                status.HTTP_400_BAD_REQUEST,
            )

        validated_data = {"returned_date": timezone.now().date()}
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=validated_data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class updateLendingView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        operation_id="Lending_GET (ID da Emprestimo)",
        description="Rota de verificação de Emprestimo, atualizando o status de todos os usuários com emprestimos caso seja necessário, retornando todos os usuários cadastrados no sistema. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Atualização de Status de todos os Usuários Necessários",
        tags=["Lending"],
    )
    def get(self, request, *args, **kwargs):
        self.check_object_permissions(request, request.user)
        lendings = Lending.objects.all()

        current_day = timezone.now()
        current_day = current_day.date()

        unblocked_date = current_day + timedelta(days=3)

        for item in lendings:
            if item.return_date < current_day and item.returned_date == None:
                validated_data = {
                    "status": "Blocked",
                    "unblocked_date": unblocked_date,
                }

                user = item.user
                user = UserStatusSerializer(
                    instance=user,
                    data=validated_data,
                    partial=True,
                )
                user.is_valid(raise_exception=True)
                user.save()

                traffic_ticket = {"traffic_ticket": " R$50,00"}
                lending = LendingsUpdateSerializer(
                    instance=item,
                    data=traffic_ticket,
                    partial=True,
                )
                lending.is_valid(raise_exception=True)
                lending.save()

                send_mail(
                    subject="Bloqueio de emprestimos KNZ Library",
                    message="Sua conta agora está bloqueada impossibilitando o emprestimo de novos livros em nossa livrária",
                    recipient_list=[user.data["email"]],
                    from_email=settings.EMAIL_HOST_USER,
                    fail_silently=False,
                )

            if item.user.unblocked_date != None:
                if item.user.unblocked_date <= current_day:
                    validated_data = {
                        "status": "Active",
                        "unblocked_date": None,
                    }

                    user = item.user
                    user = UserStatusSerializer(
                        instance=user,
                        data=validated_data,
                        partial=True,
                    )
                    user.is_valid(raise_exception=True)
                    user.save()

                    send_mail(
                        subject="Desbloqueio de emprestimos KNZ Library",
                        message="Sua conta agora está apta para realizar emprestimos em nossa livrária aproveite!!",
                        recipient_list=[user["emeil"]],
                        from_email=settings.EMAIL_HOST_USER,
                        fail_silently=False,
                    )

        return self.list(request, *args, **kwargs)


class DeleteRetriveUpdateLendingView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff]

    queryset = Lending.objects.all()
    serializer_class = LendingsUpdateSerializer

    @extend_schema(
        operation_id="Lending_GET (ID do Emprestimo)",
        description="Rota de vizualização de emprestimo, retornando o emprestimo com o mesmo ID passado na URL. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Vizualização de um Emprestimo Específico (ID do Emprestimo)",
        tags=["Lending"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="Lending_PUT (ID do Emprestimo)",
        description="Rota de atualização do emprestimo, retornando o emprestimo com o mesmo ID passado na URL. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Atualização de um Emprestimo Específico (ID do Emprestimo)",
        tags=["Lending"],
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        operation_id="Lending_PATCH (ID do Emprestimo)",
        description="Rota de atualização do emprestimo, retornando o emprestimo com o mesmo ID passado na URL. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Atualização de um Emprestimo Específico (ID do Emprestimo)",
        tags=["Lending"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        operation_id="Lending_DELETE (ID do Emprestimo)",
        description="Rota de deleção do emprestimo com o mesmo ID passado na URL, não retornando nada ao usuário. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Deleção de um Emprestimo Específico (ID do Emprestimo)",
        tags=["Lending"],
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
