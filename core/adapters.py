# core/adapters.py
from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import ValidationError


class CustomAccountAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        if not email.lower().endswith('@aluno.univesp.br'):
            raise ValidationError(
                "Cadastro permitido apenas para e-mails institucionais do domínio @aluno.univesp.br"
            )
        return super().clean_email(email)

    def save_user(self, request, user, form, commit=True):
        user.save()
        return user
