from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError(_('O Email deve ser definido'))

        email = self.normalize_email(email)

        #TODO regra de validacao do dominio @univesp.com.br -> OTP
        # if not super_user
        #       faz a validacao


        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        #TODO pular a regra de validacao de email
        # super_user = 1 -> extra_fields

        return self.create_user(email, password, **extra_fields)


