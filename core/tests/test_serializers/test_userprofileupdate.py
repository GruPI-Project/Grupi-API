from django.test import TestCase
from core.serializers import UserProfileUpdateSerializer
from core.models import (
    ProjetoIntegrador, DRP, Polo, Curso, Eixo,
    CustomUser, UserProfile, Tags
)

class UserProfileUpdateSerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="user@faculdade.edu", password="senha123")
        self.eixo = Eixo.objects.create(nome="Eixo 1")
        self.drp = DRP.objects.create(numero=1)
        self.polo = Polo.objects.create(nome="Polo", drp=self.drp)
        self.curso = Curso.objects.create(nome="Curso", eixo=self.eixo)
        self.projeto = ProjetoIntegrador.objects.create(numero=1)
        self.profile = UserProfile.objects.create(
            user=self.user,
            projeto_integrador=self.projeto,
            polo=self.polo,
            curso=self.curso
        )
        self.tags = [Tags.objects.create(name=f"Tag {i}") for i in range(3)]

    def test_update_user_profile_tags(self):
        data = {
            'polo': self.polo.id,
            'curso': self.curso.id,
            'projeto_integrador': self.projeto.id,
            'tags': [tag.id for tag in self.tags]
        }

        serializer = UserProfileUpdateSerializer(instance=self.profile, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()
        self.assertEqual(updated.tags.count(), 3)
