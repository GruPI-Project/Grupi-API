from django.test import TestCase
from core.serializers import CustomRegisterSerializer
from core.models import ProjetoIntegrador, DRP, Polo, Curso, Eixo, CustomUser, UserProfile
from rest_framework.exceptions import ValidationError

class CustomRegisterSerializerTest(TestCase):

    def setUp(self):
        self.eixo = Eixo.objects.create(nome="Tecnologia")
        self.drp = DRP.objects.create(numero=1)
        self.polo = Polo.objects.create(nome="Polo 1", drp=self.drp)
        self.curso = Curso.objects.create(nome="Curso 1", eixo=self.eixo)
        self.projeto = ProjetoIntegrador.objects.create(numero=1)

    def test_register_user_success(self):
        data = {
            'email': 'user@faculdade.edu',
            'password1': 'senha123!',
            'password2': 'senha123!',
            'first_name': 'John',
            'last_name': 'Doe',
            'projeto_integrador': self.projeto.id,
            'drp': self.drp.id,
            'polo': self.polo.id,
            'curso': self.curso.id
        }
        serializer = CustomRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save(request=None)

        self.assertEqual(user.email, 'user@faculdade.edu')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
