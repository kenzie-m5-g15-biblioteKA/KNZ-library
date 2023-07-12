from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User
from .permissions import IsAccountOwner, IsStaff
from .serializers import UserSerializer, UserStatusSerializer


class UserView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff]

    queryset = User.objects.all()
    serializer_class = UserStatusSerializer
    user = "user"

    @extend_schema(
        operation_id="Users_GET",
        description="Rota de listagem de usuários, retornando todos os usuários cadastrados no sistema. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Listagem de Usuários",
        tags=["User"],
    )
    def get(self, request, *args, **kwargs):
        self.check_object_permissions(request, request.user)
        return self.list(request, *args, **kwargs)

    @extend_schema(
        operation_id="Users_POST",
        description="Rota de criação de usuários, retornando o usuario criado e adicionando-o no banco de dados. Não é necessário autenticação",
        summary="Criação de Usuários",
        tags=["User"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    @extend_schema(
        operation_id="Users_GET (ID do Usuário)",
        description="Rota de listagem do usuário, retornando o usuário cadastrado no sistema com o mesmo ID passado na URL. É necessário estar autenticado como colaborador para acessar todos os usuarios porém todos os usuarios autenticados pódem acessar sua própria conta",
        summary="Listagem de um Usuário Específico (ID do Usuário)",
        tags=["User"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="Users_PUT (ID do Usuário)",
        description="Rota de atualização do usuário, retornando o usuário atualizado no sistema com o mesmo ID passado na URL. É necessário estar autenticado para acessar essa rota, e é apenas possivel atualizar sua própria conta",
        summary="Atualização de um Usuário Específico (ID do Usuário)",
        tags=["User"],
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        operation_id="Users_PUT (ID do Usuário)",
        description="Rota de atualização do usuário, retornando o usuário atualizado no sistema com o mesmo ID passado na URL. É necessário estar autenticado para acessar essa rota, e é apenas possivel atualizar sua própria conta",
        summary="Atualização de um Usuário Específico (ID do Usuário)",
        tags=["User"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff]

    @extend_schema(
        operation_id="Users_DELETE (ID do Usuário)",
        description="Rota de deleção do usuário com o mesmo id passado na URL, não retornando nada ao usuário. É necessário estar autenticado como colaborador para acessar essa rota",
        summary="Deleção de um Usuário (ID do Usuário)",
        tags=["User"],
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
