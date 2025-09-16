# core/adapters.py
from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import ValidationError


class CustomAccountAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        if not email.lower().endswith('@faculdade.edu'):
            raise ValidationError(
                "Cadastro permitido apenas para e-mails institucionais do domínio @faculdade.edu."
            )
        return super().clean_email(email)

    def save_user(self, request, user, form, commit=True):
        user.save()
        return user
