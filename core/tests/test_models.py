# core/tests/test_models.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from core.models import (
    CustomUser, ProjetoIntegrador, DRP, Polo, Eixo, Curso, Tags,
    ProjectGroup, ProjectGroupTags, UserProfile, Membership, JoinRequest
)

class ModelCreationTests(TestCase):

    def setUp(self):
        # Base de dados para os testes
        self.user = CustomUser.objects.create_user(email="teste@exemplo.com", password="senha123")
        self.projeto = ProjetoIntegrador.objects.create(numero=1)
        self.drp = DRP.objects.create(numero=1)
        self.polo = Polo.objects.create(nome="Polo SP", drp=self.drp)
        self.eixo = Eixo.objects.create(nome="Tecnologia")
        self.curso = Curso.objects.create(nome="Engenharia de Software", eixo=self.eixo)
        self.tags = [Tags.objects.create(name=f"Tag {i}") for i in range(1, 6)]

    def test_criacao_grupo_projeto(self):
        grupo = ProjectGroup.objects.create(
            name="Grupo 1",
            description="Descrição de teste",
            creator=self.user,
            projeto_integrador=self.projeto,
            drp=self.drp,
            polo=self.polo,
            eixo=self.eixo,
            curso=self.curso
        )
        self.assertEqual(str(grupo), "Grupo 1")

    def test_adicionar_tags_ao_grupo(self):
        grupo = ProjectGroup.objects.create(
            name="Grupo com Tags",
            creator=self.user,
            projeto_integrador=self.projeto,
            drp=self.drp,
            polo=self.polo,
            eixo=self.eixo,
            curso=self.curso
        )
        for tag in self.tags:
            ProjectGroupTags.objects.create(project_group=grupo, tag=tag)

        self.assertEqual(grupo.tags.count(), 5)

    def test_limite_tags_por_grupo(self):
        grupo = ProjectGroup.objects.create(
            name="Grupo Limite",
            creator=self.user,
            projeto_integrador=self.projeto,
            drp=self.drp,
            polo=self.polo,
            eixo=self.eixo,
            curso=self.curso
        )
        # 5 tags válidas
        for tag in self.tags:
            ProjectGroupTags.objects.create(project_group=grupo, tag=tag)

        # 6ª tag deve falhar
        sexta_tag = Tags.objects.create(name="Tag 6")
        with self.assertRaises(ValidationError):
            ProjectGroupTags.objects.create(project_group=grupo, tag=sexta_tag)

    def test_criacao_profile_usuario(self):
        profile = UserProfile.objects.create(
            user=self.user,
            projeto_integrador=self.projeto,
            polo=self.polo,
            curso=self.curso
        )
        self.assertEqual(str(profile), self.user.email)

    def test_join_request(self):
        grupo = ProjectGroup.objects.create(
            name="Grupo Join",
            creator=self.user,
            projeto_integrador=self.projeto,
            drp=self.drp,
            polo=self.polo,
            eixo=self.eixo,
            curso=self.curso
        )
        join_request = JoinRequest.objects.create(
            user=self.user,
            project_group=grupo
        )
        self.assertEqual(join_request.status, JoinRequest.Status.PENDING)

    def test_membership_criacao(self):
        grupo = ProjectGroup.objects.create(
            name="Grupo Membro",
            creator=self.user,
            projeto_integrador=self.projeto,
            drp=self.drp,
            polo=self.polo,
            eixo=self.eixo,
            curso=self.curso
        )
        membership = Membership.objects.create(
            user=self.user,
            project_group=grupo,
            role=Membership.Role.ADMIN
        )
        self.assertEqual(membership.role, "ADMIN")
        self.assertIn(self.user.email, str(membership))
