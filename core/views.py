from django.template.defaulttags import querystring
from django.http import Http404
from django.db import transaction, IntegrityError
from rest_framework import generics, serializers, permissions, status
from drf_spectacular.utils import extend_schema_field, extend_schema, extend_schema_view, OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Eixo, Polo, DRP, Curso, ProjetoIntegrador, Tags, UserProfile, UserTags, ProjectGroup, Membership, \
    CustomUser, JoinRequest
from .permissions import IsAdminOfGroup, CanRemoveMembership, IsMemberOfGroup
from .serializers import *


@extend_schema_view(
    get=extend_schema(
        summary="Listar eixos",
        description="Retorna lista de todos os eixos acadêmicos disponíveis.",
        tags=['Dados Acadêmicos'],
        responses={200: EixoSerializer(many=True)}
    )
)
class EixoListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Eixo.objects.all()
    serializer_class = EixoSerializer

@extend_schema_view(
    get=extend_schema(
        summary="Listar polos",
        description="Retorna lista de todos os polos presenciais com suas DRPs.",
        tags=['Dados Acadêmicos'],
        responses={200: PoloSerializer(many=True)}
    )
)
class PoloListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Polo.objects.all()
    serializer_class = PoloSerializer

@extend_schema_view(
    get=extend_schema(
        summary="Listar DRPs",
        description="Retorna lista de todas as Diretorias Regionais de Polo (DRP 1-14).",
        tags=['Dados Acadêmicos'],
        responses={200: DRPSerializer(many=True)}
    )
)
class DRPListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DRP.objects.all()
    serializer_class = DRPSerializer

@extend_schema_view(
    get=extend_schema(
        summary="Listar cursos",
        description="Retorna lista de todos os cursos com seus eixos.",
        tags=['Dados Acadêmicos'],
        responses={200: CursoSerializer(many=True)}
    )
)
class CursoListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

@extend_schema_view(
    get=extend_schema(
        summary="Listar Projetos Integradores",
        description="Retorna lista de Projetos Integradores (PI 1-6).",
        tags=['Dados Acadêmicos'],
        responses={200: ProjetoIntegradorSerializer(many=True)}
    )
)
class ProjetoIntegradorListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ProjetoIntegrador.objects.all()
    serializer_class = ProjetoIntegradorSerializer

@extend_schema_view(
    get=extend_schema(
        summary="Listar tags",
        description="Retorna lista de todas as tags de habilidades/interesses disponíveis.",
        tags=['Dados Acadêmicos'],
        responses={200: TagSerializer(many=True)}
    )
)
class TagsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Tags.objects.all()
    serializer_class = TagSerializer

@extend_schema_view(
    get=extend_schema(
        summary="Obter perfil próprio",
        description="Retorna o perfil completo do usuário autenticado.",
        tags=['Perfil de Usuário'],
        responses={200: UserProfileDetailSerializer}
    ),
    patch=extend_schema(
        summary="Atualizar perfil próprio",
        description="Atualiza polo, curso, PI e tags do perfil do usuário.",
        tags=['Perfil de Usuário'],
        request=UserProfileUpdateSerializer,
        responses={
            200: UserProfileDetailSerializer,
            400: OpenApiResponse(description="Dados inválidos")
        }
    )
)
class ProfileSelfView(generics.RetrieveUpdateAPIView):
    http_method_names = ['get', 'patch', 'head', 'options']
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileDetailSerializer

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UserProfileUpdateSerializer
        return UserProfileDetailSerializer

    def get_object(self):
        return self.request.user.profile

@extend_schema_view(
    get=extend_schema(
        summary="Obter perfil de outro usuário",
        description="Retorna o perfil de um usuário específico pelo ID.",
        tags=['Perfil de Usuário'],
        parameters=[
            OpenApiParameter(
                name='user',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='UUID do usuário'
            )
        ],
        responses={
            200: UserProfileDetailSerializer,
            404: OpenApiResponse(description="Usuário não encontrado")
        }
    )
)
class ProfileDetailsView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer
    lookup_field = 'user'

@extend_schema_view(
    get=extend_schema(
        summary="Listar tags do usuário",
        description="Retorna todas as tags associadas ao perfil do usuário autenticado.",
        tags=['Perfil de Usuário'],
        responses={200: TagSerializer(many=True)}
    )
)
class UserTagsListView(generics.ListAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = self.request.user.profile
        return profile.tags.all()

@extend_schema_view(
    get=extend_schema(
        summary="Listar grupos de projeto",
        description="Retorna lista de todos os grupos de projeto.",
        tags=['Grupos de Projeto'],
        responses={200: ProjectGroupSerializer(many=True)}
    ),
    post=extend_schema(
        summary="Criar grupo de projeto",
        description=(
            "Cria um novo grupo de projeto. O usuário autenticado será o criador e admin do grupo. "
            "Informações acadêmicas (PI, DRP, Polo, Eixo, Curso) são herdadas automaticamente do perfil do criador.\n\n"
            "**Validações:**\n"
            "- Usuário não pode estar em outro grupo\n"
            "- Máximo de 5 tags por grupo"
        ),
        tags=['Grupos de Projeto'],
        request=ProjectGroupSerializer,
        responses={
            201: ProjectGroupSerializer,
            400: OpenApiResponse(description="Erro de validação (usuário já em grupo, etc)")
        }
    )
)
class ProjectGroupView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options']
    queryset = ProjectGroup.objects.all()
    serializer_class = ProjectGroupSerializer

    def create(self, request, *args, **kwargs):
        user_is_already_in_a_group = Membership.objects.filter(user=self.request.user).exists()
        if user_is_already_in_a_group:
            raise serializers.ValidationError(
                {'detail': 'Você já faz parte de um grupo e não pode criar outro.'}
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        profile = self.request.user.profile
        with transaction.atomic():
            project_group_instance = serializer.save(
                creator=self.request.user,
                projeto_integrador=profile.projeto_integrador,
                drp=profile.polo.drp,
                polo=profile.polo,
                eixo=profile.curso.eixo,
                curso=profile.curso,
            )

            membership_instance = Membership.objects.create(
                user=self.request.user,
                project_group=project_group_instance,
                role=Membership.Role.ADMIN,
            )

@extend_schema_view(
    get=extend_schema(
        summary="Obter detalhes de um grupo",
        description="Retorna informações completas de um grupo específico.",
        tags=['Grupos de Projeto'],
        responses={
            200: ProjectGroupSerializer,
            404: OpenApiResponse(description="Grupo não encontrado")
        }
    ),
    patch=extend_schema(
        summary="Atualizar grupo",
        description=(
            "Atualiza nome, descrição e tags do grupo.\n\n"
            "**Permissões:** Apenas o admin do grupo pode atualizar"
        ),
        tags=['Grupos de Projeto'],
        request=ProjectGroupUpdateSerializer,
        responses={
            200: ProjectGroupSerializer,
            400: OpenApiResponse(description="Dados inválidos"),
            403: OpenApiResponse(description="Sem permissão (não é admin do grupo)"),
            404: OpenApiResponse(description="Grupo não encontrado")
        }
    ),
    delete=extend_schema(
        summary="Deletar grupo",
        description=(
            "Remove o grupo de projeto.\n\n"
            "**Permissões:** Apenas o admin do grupo pode deletar"
        ),
        tags=['Grupos de Projeto'],
        responses={
            204: OpenApiResponse(description="Grupo deletado com sucesso"),
            403: OpenApiResponse(description="Sem permissão (não é admin do grupo)"),
            404: OpenApiResponse(description="Grupo não encontrado")
        }
    )
)
class ProjectGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ['get', 'patch', 'delete','head', 'options']
    permission_classes = [IsAuthenticated,IsAdminOfGroup]
    queryset = ProjectGroup.objects.all()
    serializer_class = ProjectGroupSerializer

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return ProjectGroupUpdateSerializer
        return  super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        if response.status_code == 200:
            instance = self.get_object()
            full_serializer = ProjectGroupSerializer(instance, context=self.get_serializer_context())
            response.data = full_serializer.data

        return response

@extend_schema_view(
    get=extend_schema(
        summary="Listar membros do grupo",
        description="Retorna lista de membros do grupo com seus IDs de usuário e roles.",
        tags=['Grupos de Projeto'],
        parameters=[
            OpenApiParameter(
                name='group_pk',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID do grupo'
            )
        ],
        responses={
            200: MembershipUserIdSerializer(many=True),
            404: OpenApiResponse(description="Grupo não encontrado")
        }
    )
)
class ProjectGroupMembersListView(generics.ListAPIView):
    serializer_class = MembershipUserIdSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        group_pk = self.kwargs['group_pk']
        return Membership.objects.filter(project_group__pk=group_pk)

@extend_schema_view(
    get=extend_schema(
        summary="Obter grupo do usuário",
        description="Retorna o grupo de projeto do qual o usuário faz parte.",
        tags=['Grupos de Projeto'],
        responses={
            200: ProjectGroupSerializer,
            404: OpenApiResponse(description='Usuário não faz parte de nenhum grupo')
        }
    )
)
class ProjectGroupSelfView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectGroupSerializer
    queryset = ProjectGroup.objects.all()

    def get_object(self):
        try:
            membership = self.request.user.membership
            return membership.project_group
        except Membership.DoesNotExist:
            raise Http404('Você não faz parte de nenhum grupo.')

class MembershipDeleteView(APIView):
    permission_classes = [IsAuthenticated, CanRemoveMembership]


    def get_object(self, group_pk, user_pk):
        group = get_object_or_404(ProjectGroup, pk=group_pk)
        user = get_object_or_404(CustomUser, pk=user_pk)

        # Retorna o objeto Membership que será o alvo
        return get_object_or_404(Membership, project_group=group, user=user)

    @extend_schema(
        summary="Remover membro do grupo",
        description=(
            "Remove um membro específico do grupo.\n\n"
            "**Permissões:**\n"
            "- Admin do grupo pode remover qualquer membro\n"
            "- Membro pode se remover (auto-remoção)"
        ),
        tags=['Grupos de Projeto'],
        parameters=[
            OpenApiParameter(
                name='group_pk',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID do grupo'
            ),
            OpenApiParameter(
                name='user_pk',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='UUID do usuário a ser removido'
            )
        ],
        request=None,
        responses={
            204: OpenApiResponse(description="Membro removido com sucesso"),
            403: OpenApiResponse(response=MessageResponseSerializer, description="Sem permissão para remover este membro"),
            404: OpenApiResponse(description="Grupo, usuário ou membership não encontrado"),
        }
    )
    def delete(self, request, group_pk, user_pk, format=None):
        membership_to_delete = self.get_object(group_pk, user_pk)

        self.check_object_permissions(self.request, membership_to_delete)

        membership_to_delete.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class LeaveGroupView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Sair do grupo",
        description=(
            "Remove o usuário autenticado do grupo atual.\n\n"
            "**Validações:**\n"
            "- Usuário deve fazer parte de um grupo\n"
            "- Admin/criador não pode sair (deve deletar o grupo)"
        ),
        tags=['Grupos de Projeto'],
        request=None,
        responses={
            204: OpenApiResponse(description="Saiu do grupo com sucesso"),
            400: OpenApiResponse(response=MessageResponseSerializer,
                                 description="Usuário não faz parte de nenhum grupo"),
            403: OpenApiResponse(response=MessageResponseSerializer,
                                 description="Admin não pode sair do grupo"),
        }
    )
    def post(self, request, format=None):
        try:
            membership_to_delete = request.user.membership
        except Membership.DoesNotExist:
            return Response(
                {'detail': 'Você não faz parte de nenhum grupo.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = request.user
        group = membership_to_delete.project_group
        if group.creator == user:
            return Response(
                {'detail': 'O administrador não pode sair do grupo. O grupo deve ser deletado.'},
                status=status.HTTP_403_FORBIDDEN
            )

        membership_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class JoinGroupView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Solicitar entrada em grupo",
        description=(
            "Permite que um usuário solicite entrada em um grupo de projeto.\n\n"
            "**Comportamento:**\n"
            "- Se o grupo não for moderado, o usuário entra imediatamente\n"
            "- Se o grupo for moderado, cria um pedido de entrada pendente\n\n"
            "**Validações:**\n"
            "- Usuário não pode estar em outro grupo\n"
            "- Grupo deve existir e estar ativo"
        ),
        tags=['Grupos de Projeto'],
        parameters=[
            OpenApiParameter(
                name='group_pk',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID do grupo'
            )
        ],
        request=None,
        responses={
            201: OpenApiResponse(response=MessageResponseSerializer, description="Entrou no grupo com sucesso (grupo não moderado)"),
            202: OpenApiResponse(response=MessageResponseSerializer, description="Pedido de entrada criado (grupo moderado)"),
            400: OpenApiResponse(response=MessageResponseSerializer, description="Usuário já está em um grupo ou já tem pedido pendente"),
            404: OpenApiResponse(description="Grupo não encontrado"),
        }
    )
    def post(self, request, group_pk, format=None):
        user = self.request.user
        group = get_object_or_404(ProjectGroup, pk=group_pk)

        user_is_already_in_a_group = Membership.objects.filter(user=user).exists()
        if user_is_already_in_a_group:
            return Response(
                {'detail': 'Você já faz parte de um grupo e não pode entrar em outro.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_aready_asked_to_join_this_group = JoinRequest.objects.filter(
            user=user,
            project_group=group,
            status=JoinRequest.Status.PENDING,
        ).exists()
        if user_aready_asked_to_join_this_group:
            return Response(
                {'detail': 'Você já enviou uma solicitação para entrar neste grupo. Aguarde a aprovação.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        #se o grupo for moderado solicita a entrada criando uma joinrequest pending
        if group.moderated:
            JoinRequest.objects.create(
                user=user,
                project_group=group,
                status=JoinRequest.Status.PENDING,
            )
            return Response(
                {'detail': 'Solicitação enviada. Aguarde a aprovação do administrador do grupo.'},
                status=status.HTTP_202_ACCEPTED
            )
        #se o grupo nao for moderado entra direto no grupo (usa transaction para criar os 2 objetos)
        else:
            try:
                with transaction.atomic():
                    Membership.objects.create(
                        user=user,
                        project_group=group,
                        role=Membership.Role.MEMBER,
                    )
                    JoinRequest.objects.create(
                        user=user,
                        project_group=group,
                        status=JoinRequest.Status.APPROVED,
                    )
                return Response(
                    {'detail': 'Você entrou no grupo com sucesso.'},
                    status=status.HTTP_201_CREATED
                )

            except IntegrityError:
                return Response(
                    {'detail': 'Erro ao entrar no grupo. Tente novamente mais tarde.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

@extend_schema_view(
    get=extend_schema(
        summary="Listar pedidos de entrada do grupo",
        description=(
            "Retorna todos os pedidos de entrada pendentes para o grupo do usuário autenticado.\n\n"
            "**Permissões:** Apenas admins de grupos podem ver pedidos"
        ),
        tags=['Pedidos de Entrada'],
        parameters=[
            OpenApiParameter(
                name='group_pk',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID do grupo'
            )
        ],
        responses={
            200: JoinRequestSerializer(many=True),
            403: OpenApiResponse(description="Usuário não é admin de nenhum grupo")
        }
    )
)
class JoinRequestListView(generics.ListAPIView):
    """
    Lista todas as solicitações de entrada pendentes para um grupo específico.
    """
    permission_classes = [IsAuthenticated, IsMemberOfGroup]
    serializer_class = JoinRequestSerializer

    def get_queryset(self):
        group_pk = self.request.user.membership.project_group.pk
        group = get_object_or_404(ProjectGroup, pk=group_pk)
        return JoinRequest.objects.filter(project_group=group, status=JoinRequest.Status.PENDING)

class JoinRequestApproveView(APIView):

    permission_classes = [IsAuthenticated, IsAdminOfGroup]

    @extend_schema(
        summary="Aprovar pedido de entrada",
        description=(
            "Aprova um pedido de entrada, adicionando o usuário ao grupo.\n\n"
            "**Permissões:** Apenas o admin do grupo pode aprovar"
        ),
        tags=['Pedidos de Entrada'],
        parameters=[
            OpenApiParameter(
                name='request_pk',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID do pedido de entrada'
            )
        ],
        request=None,
        responses={
            200: OpenApiResponse(
                response=MessageResponseSerializer,
                description="Pedido aprovado com sucesso"
            ),
            400: OpenApiResponse(
                response=MessageResponseSerializer,
                description="Pedido já foi processado ou usuário já está em grupo"
            ),
            403: OpenApiResponse(
                response=MessageResponseSerializer,
                description="Sem permissão para aprovar este pedido"
            ),
            404: OpenApiResponse(
                description="Pedido não encontrado"
            ),
        }
    )
    def post(self, request, request_pk, format=None):
        join_request = get_object_or_404(JoinRequest, pk=request_pk)

        self.check_object_permissions(self.request, join_request.project_group)

        user = join_request.user
        group = join_request.project_group

        #se um user ja estiver em um grupo rejeita a solicitação automaticamente
        user_is_already_in_a_group = Membership.objects.filter(user=user).exists()
        if user_is_already_in_a_group:
            join_request.status = JoinRequest.Status.REJECTED
            join_request.save()
            return Response(
                {'detail': 'O usuário já faz parte de outro grupo. A solicitação foi rejeitada.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                Membership.objects.create(
                    user=user,
                    project_group=group,
                    role=Membership.Role.MEMBER,
                )
                join_request.status = JoinRequest.Status.APPROVED
                join_request.save()

            return Response(
                {'detail': 'Solicitação aprovada. O usuário agora é membro do grupo.'},
                status=status.HTTP_200_OK
            )

        except IntegrityError:
            return Response(
                {'detail': 'Erro ao aprovar a solicitação. Tente novamente mais tarde.'},
                status=status.HTTP_400_BAD_REQUEST
            )

class JoinRequestRejectView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOfGroup]

    @extend_schema(
        summary="Rejeitar pedido de entrada",
        description=(
            "Rejeita um pedido de entrada.\n\n"
            "**Permissões:** Apenas o admin do grupo pode rejeitar"
        ),
        tags=['Pedidos de Entrada'],
        parameters=[
            OpenApiParameter(
                name='request_pk',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID do pedido de entrada'
            )
        ],
        request=None,
        responses={
            200: OpenApiResponse(response=MessageResponseSerializer, description="Pedido rejeitado com sucesso"),
            400: OpenApiResponse(response=MessageResponseSerializer, description="Pedido já foi processado"),
            403: OpenApiResponse(response=MessageResponseSerializer, description="Sem permissão para rejeitar este pedido"),
            404: OpenApiResponse(description="Pedido não encontrado"),
        }
    )
    def post(self, request, request_pk, format=None):
        join_request = get_object_or_404(JoinRequest, pk=request_pk)

        self.check_object_permissions(self.request, join_request.project_group)

        # se a solicitação já foi processada, retorna erro
        if join_request.status != JoinRequest.Status.PENDING:
            return Response(
                {'detail': 'Esta solicitação já foi processada.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        join_request.status = JoinRequest.Status.REJECTED
        join_request.save()

        return Response(
            {'detail': 'Solicitação rejeitada com sucesso.'},
            status=status.HTTP_200_OK
        )

@extend_schema_view(
    get=extend_schema(
        summary="Obter pedidos de entrada próprios",
        description="Retorna todos os pedidos de entrada do usuário autenticado.",
        tags=['Pedidos de Entrada'],
        responses={
            200: JoinRequestSerializer(many=True),
            404: OpenApiResponse(description="Usuário não tem pedidos de entrada")
        }
    )
)
class JoinRequestSelfView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JoinRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return JoinRequest.objects.filter(user=user)