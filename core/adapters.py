# core/adapters.py
from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import redirect


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

    def respond_user_inactive(self, request, user):
        """
        Override the default behavior for inactive users to return JSON response
        instead of redirecting to a web view. This is needed for API registration
        to work properly with dj_rest_auth.
        """
        return JsonResponse({
            'detail': 'Sua conta ainda não foi ativada.',
            'message': 'Você precisa verificar seu email antes de fazer o primeiro login. '
                      'Verifique sua caixa de entrada e clique no link de verificação, '
                      'ou solicite um novo código de verificação.',
            'code': 'account_inactive',
            'user_id': str(user.id) if user else None
        }, status=400)
