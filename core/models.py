from doctest import master

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _


#Modelo de Autenticacao customizado para usar o email
class CustomUser(AbstractUser):

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

#Modelos de Estrutura Academica / ENUNS mapeados
class ProjetoIntegrador(models.Model):
    numero = models.PositiveSmallIntegerField(
        unique=True,
        verbose_name="Numero do Projeto Integrador",
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )

    class Meta:
        ordering = ['numero']
        verbose_name = "Projeto Integrador"
        verbose_name_plural = "Projetos Integradores"

    def __str__(self):
        return f"PI {self.numero}"

class DRP(models.Model):
    #numero vai de 1 - 14
    numero = models.PositiveSmallIntegerField(
        unique=True,
        verbose_name="Numero do DRP",
        validators=[MinValueValidator(1), MaxValueValidator(14)],
    )
    nome = models.CharField(
        unique=True,
        max_length=100,
        verbose_name="Regioes",
    )

    class Meta:
        ordering = ['numero']
        verbose_name = "DRP"
        verbose_name_plural = "DRPs"

    def __str__(self):
        return f"DRP {self.numero} - {self.nome}"

class Polo(models.Model):
    nome = models.CharField(unique=False, max_length=100)
    drp = models.ForeignKey(DRP, on_delete=models.PROTECT, related_name='polos')

    class Meta:
        verbose_name = "Polo"
        verbose_name_plural = "Polos"

    def __str__(self):
        return self.nome

class Eixo(models.Model):
    nome = models.CharField(
        unique=True,
        max_length=100,
    )

    class Meta:
        verbose_name = "Eixo"
        verbose_name_plural = "Eixos"
    def __str__(self):
        return self.nome

class Curso(models.Model):
    nome = models.CharField(unique=True,max_length=150)
    eixo = models.ForeignKey(Eixo, on_delete=models.PROTECT, related_name='cursos')

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.nome

class Tags(models.Model):
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name

# Project_group
class ProjectGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, verbose_name="Nome Do Grupo")
    description = models.TextField(blank=True, null=True, verbose_name="Descricao do Grupo")
    creator = models.ForeignKey(
        CustomUser,
        #TODO VALIDAR RELATED NAME
        related_name="grupos",
        on_delete=models.PROTECT,
    )
    projeto_integrador = models.ForeignKey(
        ProjetoIntegrador,
        related_name="grupos",
        on_delete=models.PROTECT,
    )

    drp = models.ForeignKey(
        DRP,
        related_name="grupos",
        on_delete=models.PROTECT,
    )

    polo = models.ForeignKey(
        Polo,
        related_name="grupos",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    eixo = models.ForeignKey(
        Eixo,
        related_name="grupos",
        on_delete=models.PROTECT,
    )

    curso = models.ForeignKey(
        Curso,
        related_name="grupos",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class JoinPolicy(models.TextChoices):
        OPEN = 'OPEN', 'Aberto'
        MODERATE = 'MODERATE', 'Moderado'

    join_policy = models.CharField(
        max_length=20,
        verbose_name="Politica de entrada",
        choices=JoinPolicy.choices,
        default=JoinPolicy.MODERATE
    )

    class Meta:
        verbose_name = "Grupo de PI"
        verbose_name_plural = "Grupos de PI"

    def __str__(self):
        return self.name

# Classe de dados que vai controlar o profile do usuario
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    projeto_integrador = models.ForeignKey(
        ProjetoIntegrador,
        on_delete=models.PROTECT,
        related_name='alunos',
        null=True
    )
    drp = models.ForeignKey(
       DRP,
       related_name="alunos",
       on_delete=models.PROTECT,
       null=True
    )
    polo = models.ForeignKey(
       Polo,
       related_name="alunos",
       on_delete=models.PROTECT,
       null=True
    )
    curso = models.ForeignKey(
        Curso,
        related_name="alunos",
        on_delete=models.PROTECT,
    )

    eixo = models.ForeignKey(
        Eixo,
        related_name="alunos",
        on_delete=models.PROTECT,
    )
    class Meta:
        verbose_name = "Profile de Usuario"
        verbose_name_plural = "Profiles de Usuarios"

    def __str__(self):
        return self.user.email

#Classe responsavel pelos membros de cada grupo
class Membership(models.Model):
        #classe com as roles permitidas
        class Role(models.TextChoices):
            MEMBER = 'MEMBER', 'Membro'
            ADMIN = 'ADMIN', 'Admin'

        user = models.OneToOneField(
            CustomUser,
            on_delete=models.CASCADE,
            related_name='membership'
        )
        project_group = models.ForeignKey(
            ProjectGroup,
            on_delete=models.CASCADE,
            related_name='memberships',
        )

        role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)

        date_joined = models.DateField(auto_now_add=True)
        class Meta:
            verbose_name = "Vinculo de Membro"
            verbose_name_plural = "Vinculo de Membros"

        def __str__(self):
            return f"{self.user.email} em {self.project_group.name}"

# Join_request - pedido de entrada em um grupo
class JoinRequest(models.Model):

    #Classe que vai conter os estados possiveis na tabela
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pendente'
        APPROVED = 'APPROVED', 'Aprovado'
        REJECTED = 'REJECTED', 'Rejetado'

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='join_requests',
    )
    project_group = models.ForeignKey(
        ProjectGroup,
        on_delete=models.CASCADE,
        related_name='join_requests',
    )
    date_requested = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    class Meta:
        #garantir que somente 1 pedido de entrada em cada grupo
        unique_together = ('user', 'project_group')
        verbose_name = "Pedido de entrada"
        verbose_name_plural = "Pedidos de entrada"

    def __str__(self):
        return f"Pedido de {self.user.email} para {self.project_group.name}"

# user_tags - vinculo entre o user profile e as tags escolidas
class UserTags(models.Model):
    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
    )

    class Meta:
        #somente permite 1 tag unica para cada profile
        unique_together = ('profile', 'tag')
        verbose_name = "Tags do usuario"
        verbose_name_plural = "Tags dos usuarios"

    def __str__(self):
        return f"#{self.tag}"

# project_group_tags vinculo entre o grupo e as tags escolidas
class ProjectGroupTags(models.Model):
    project_group = models.ForeignKey(
        ProjectGroup,
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('project_group', 'tag')
        verbose_name = "Tags do grupo"
        verbose_name_plural = "Tags dos grupos"

    def __str__(self):
        return f"#{self.tag}"