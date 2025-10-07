from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.models import CustomUser, ProjetoIntegrador, DRP, Polo, Curso, Eixo, UserProfile, ProjectGroup, Membership, Tags

class ViewsTestCase(APITestCase):
    def setUp(self):
        # Cria objetos base para os testes
        self.user = CustomUser.objects.create_user(email='user@test.com', password='senha123')
        self.client.force_authenticate(user=self.user)  # Autentica o client para usar nas requisições

        self.eixo = Eixo.objects.create(nome="Eixo 1")
        self.drp = DRP.objects.create(numero=1)
        self.polo = Polo.objects.create(nome="Polo 1", drp=self.drp)
        self.curso = Curso.objects.create(nome="Curso 1", eixo=self.eixo)
        self.projeto = ProjetoIntegrador.objects.create(numero=1)
        self.profile = UserProfile.objects.create(
            user=self.user, projeto_integrador=self.projeto,
            polo=self.polo, curso=self.curso
        )
        self.tags = Tags.objects.bulk_create([
            Tags(name='Tag 1'),
            Tags(name='Tag 2'),
            Tags(name='Tag 3')
        ])

    def test_eixo_list(self):
        url = reverse('core:eixo-list')  # Ajuste conforme o nome da url
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_profile_self_get_and_patch(self):
        url = reverse('core:profile-me')  # Ajuste o nome conforme sua urls.py

        # GET - Deve retornar os dados do perfil do usuário autenticado
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('polo', response.data)

        # PATCH - Atualizar tags do perfil
        tag_ids = [tag.id for tag in self.tags]
        patch_data = {
            "tags": tag_ids,
            "polo": self.polo.id,
            "curso": self.curso.id,
            "projeto_integrador": self.projeto.id
        }
        response = self.client.patch(url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.tags.count(), len(self.tags))

    def test_create_project_group_prevent_if_already_member(self):
        # Cria um grupo para o usuário
        group = ProjectGroup.objects.create(
            name="Grupo 1",
            creator=self.user,
            projeto_integrador=self.projeto,
            drp=self.drp,
            polo=self.polo,
            eixo=self.eixo,
            curso=self.curso
        )
        Membership.objects.create(user=self.user, project_group=group, role=Membership.Role.ADMIN)

        url = reverse('core:project-group-list')  # Ajuste para o nome correto da rota
        data = {
            'name': 'Novo grupo',
            'description': 'Descrição do grupo',
            'tags': [tag.id for tag in self.tags]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)

    def test_leave_group(self):
        # Cria grupo e associar usuário como admin
        group = ProjectGroup.objects.create(
            name="Grupo para sair",
            creator=self.user,
            projeto_integrador=self.projeto,
            drp=self.drp,
            polo=self.polo,
            eixo=self.eixo,
            curso=self.curso
        )
        Membership.objects.create(user=self.user, project_group=group, role=Membership.Role.ADMIN)

        url = reverse('core:project-group-leave')  # Ajuste o nome da url
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.data)

        # Cria usuário comum que pode sair do grupo
        user2 = CustomUser.objects.create_user(email='user2@test.com', password='senha123')
        Membership.objects.create(user=user2, project_group=group, role=Membership.Role.MEMBER)
        self.client.force_authenticate(user=user2)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
