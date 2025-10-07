from django.test import TestCase
from django.core.exceptions import ValidationError
from core.adapters import CustomAccountAdapter


class CustomAccountAdapterTests(TestCase):
    def setUp(self):
        self.adapter = CustomAccountAdapter()

    def test_clean_email_valido(self):
        email = "aluno@faculdade.edu"
        cleaned = self.adapter.clean_email(email)
        self.assertEqual(cleaned, email)

    def test_clean_email_invalido(self):
        emails_invalidos = [
            "teste@gmail.com",
            "usuario@outlook.com",
            "aluno@faculdade.com",
            "professor@universidade.edu",
            "admin@FACULDADE.EDU.BR",  # domínio incorreto
            "aluno@faculdade.edu.br",  # domínio diferente
            "aluno@faculdade.edu.com", # domínio composto
        ]

        for email in emails_invalidos:
            with self.subTest(email=email):
                with self.assertRaises(ValidationError) as context:
                    self.adapter.clean_email(email)

                self.assertIn("@faculdade.edu", str(context.exception))

    def test_clean_email_maiusculo_valido(self):
        # Deve aceitar mesmo se vier com letras maiúsculas
        email = "Aluno@Faculdade.edu"
        cleaned = self.adapter.clean_email(email)
        self.assertEqual(cleaned, email)
