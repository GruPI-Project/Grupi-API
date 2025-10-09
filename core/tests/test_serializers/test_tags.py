from django.test import TestCase
from core.models import *
from core.serializers import ProjectGroupSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()

class ProjectGroupSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="admin@faculdade.edu", password="senha123")
        self.eixo = Eixo.objects.create(nome="Eixo 1")
        self.drp = DRP.objects.create(numero=1)
        self.polo = Polo.objects.create(nome="Polo", drp=self.drp)
        self.curso = Curso.objects.create(nome="Curso", eixo=self.eixo)
        self.projeto = ProjetoIntegrador.objects.create(numero=1)

    def test_validate_too_many_tags(self):
        tags = [Tags.objects.create(name=f"Tag {i}") for i in range(6)]  # 6 tags
        data = {
            'name': 'Grupo A',
            'description': 'Desc',
            'creator': self.user.id,
            'tags': [tag.id for tag in tags]
        }

        group = ProjectGroup.objects.create(
            name="Grupo Teste",
            description="Desc",
            creator=self.user,
            projeto_integrador=self.projeto,
            drp=self.drp,
            polo=self.polo,
            eixo=self.eixo,
            curso=self.curso
        )

        serializer = ProjectGroupSerializer(instance=group, data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('tags', serializer.errors)
