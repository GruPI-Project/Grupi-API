from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from core.models import ProjectGroup, Membership, DRP, Polo, Eixo, Curso, ProjetoIntegrador
from core.permissions import IsAdminOfGroup, CanRemoveMembership

User = get_user_model()

class PermissionTests(TestCase):
    def setUp(self):
        # Usuários
        self.admin_user = User.objects.create_user(email="admin@faculdade.edu", password="senha123")
        self.member_user = User.objects.create_user(email="membro@faculdade.edu", password="senha123")
        self.third_user = User.objects.create_user(email="outro@faculdade.edu", password="senha123")

        # Estrutura básica
        self.drp = DRP.objects.create(numero=1)
        self.polo = Polo.objects.create(nome="Polo A", drp=self.drp)
        self.eixo = Eixo.objects.create(nome="Tecnologia")
        self.curso = Curso.objects.create(nome="Engenharia", eixo=self.eixo)
        self.projeto = ProjetoIntegrador.objects.create(numero=1)

        # Grupo
        self.group = ProjectGroup.objects.create(
            name="Grupo Teste",
            description="Desc",
            creator=self.admin_user,
            projeto_integrador=self.projeto,
            drp=self.drp,
            polo=self.polo,
            eixo=self.eixo,
            curso=self.curso
        )

        # Memberships
        self.admin_membership = Membership.objects.create(user=self.admin_user, project_group=self.group, role=Membership.Role.ADMIN)
        self.member_membership = Membership.objects.create(user=self.member_user, project_group=self.group, role=Membership.Role.MEMBER)

        # Request factory
        self.factory = APIRequestFactory()

    def test_is_admin_of_group_permission(self):
        permission = IsAdminOfGroup()

        # Admin pode editar
        request = self.factory.put('/')
        request.user = self.admin_user
        self.assertTrue(permission.has_object_permission(request, None, self.group))

        # Membro comum NÃO pode editar
        request.user = self.member_user
        self.assertFalse(permission.has_object_permission(request, None, self.group))

        # Usuário fora do grupo NÃO pode editar
        request.user = self.third_user
        self.assertFalse(permission.has_object_permission(request, None, self.group))

        # Todos podem "ver" (método seguro)
        request = self.factory.get('/')
        request.user = self.third_user
        self.assertTrue(permission.has_object_permission(request, None, self.group))

    def test_can_remove_membership_permission(self):
        permission = CanRemoveMembership()

        # Admin tentando remover membro — permitido
        request = self.factory.delete('/')
        request.user = self.admin_user
        self.assertTrue(permission.has_object_permission(request, None, self.member_membership))

        # Membro tentando sair — permitido
        request.user = self.member_user
        self.assertTrue(permission.has_object_permission(request, None, self.member_membership))

        # Admin tentando se remover — NEGADO
        request.user = self.admin_user
        self.assertFalse(permission.has_object_permission(request, None, self.admin_membership))

        # Outro usuário tentando remover membro — NEGADO
        request.user = self.third_user
        self.assertFalse(permission.has_object_permission(request, None, self.member_membership))
