from django.template.defaulttags import querystring
from django.http import Http404
from django.db import transaction
from rest_framework import generics, serializers, permissions, status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Eixo, Polo, DRP, Curso, ProjetoIntegrador, Tags, UserProfile, UserTags, ProjectGroup, Membership, \
    CustomUser
from .permissions import IsAdminOfGroup, CanRemoveMembership
from .serializers import EixoSerializer, PoloSerializer, DRPSerializer, CursoSerializer, ProjetoIntegradorSerializer, \
    TagSerializer, UserProfileSerializer, UserProfileDetailSerializer, UserProfileUpdateSerializer, \
    ProjectGroupSerializer, ProjectGroupUpdateSerializer, ProjectGroupMembersUserIdSerializer


class EixoListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Eixo.objects.all()
    serializer_class = EixoSerializer

class PoloListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Polo.objects.all()
    serializer_class = PoloSerializer

class DRPListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DRP.objects.all()
    serializer_class = DRPSerializer

class CursoListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class ProjetoIntegradorListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ProjetoIntegrador.objects.all()
    serializer_class = ProjetoIntegradorSerializer

class TagsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Tags.objects.all()
    serializer_class = TagSerializer

class ProfileSelfView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileDetailSerializer

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UserProfileUpdateSerializer
        return UserProfileDetailSerializer

    def get_object(self):
        return self.request.user.profile

class ProfileDetailsView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer
    lookup_field = 'user'

class UserTagsListView(generics.ListAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = self.request.user.profile
        return profile.tags.all()

class ProjectGroupView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
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

class ProjectGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
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

class ProjectGroupMembersView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ProjectGroup.objects.all()
    serializer_class = ProjectGroupMembersUserIdSerializer


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

    def delete(self, request, group_pk, user_pk, format=None):
        membership_to_delete = self.get_object(group_pk, user_pk)

        self.check_object_permissions(self.request, membership_to_delete)

        membership_to_delete.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class LeaveGroupView(APIView):
    permission_classes = [IsAuthenticated]

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