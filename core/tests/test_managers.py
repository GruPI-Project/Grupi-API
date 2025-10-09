from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from core.models import CustomUser

class CustomUserManagerTests(TestCase):

    def setUp(self):
        self.UserModel = get_user_model()

    def test_create_user_success(self):
        user = self.UserModel.objects.create_user(email="teste@faculdade.edu", password="senha123")
        self.assertEqual(user.email, "teste@faculdade.edu")
        self.assertTrue(user.check_password("senha123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError) as context:
            self.UserModel.objects.create_user(email=None, password="senha123")
        self.assertIn("O Email deve ser definido", str(context.exception))

    def test_email_is_normalized(self):
        email = "TestEmail@Faculdade.EDU"
        user = self.UserModel.objects.create_user(email=email, password="senha123")
        self.assertEqual(user.email, "TestEmail@faculdade.edu")  # o normalize_email só baixa o domínio

    def test_create_superuser_success(self):
        superuser = self.UserModel.objects.create_superuser(email="admin@faculdade.edu", password="admin123")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.check_password("admin123"))
