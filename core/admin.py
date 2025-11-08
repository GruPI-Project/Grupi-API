from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp
from rest_framework.authtoken.models import TokenProxy

from .models import *

#Inlines servem para que possamos ver melhor a relacao entre as tabelas
class UserProfileInline(admin.StackedInline):
    """Inline que vai permitir a visualizacao do UserProfile diretamente na pagina do CustonUser"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile de Usuarios"
    fk_name = 'user'
    show_change_link = True

class ProjectGroupTagsInline(admin.StackedInline):
    model = ProjectGroupTags
    can_delete = False
    max_num = 5
    fk_name = 'project_group'

class UserTagsInline(admin.StackedInline):
    model = UserTags
    can_delete = False
    max_num = 5
    fk_name = 'profile'

class MembershipInline(admin.StackedInline):
    model = Membership
    can_delete = True
    extra = 0

class JoinRequestInline(admin.StackedInline):
    model = JoinRequest
    can_delete = True
    extra = 1

admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.unregister(TokenProxy)
admin.site.unregister([SocialAccount, SocialToken, SocialApp])


# Melhor visualizacao para a tabela de usuario (aqui que o userprofile inline vai)
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        # ESTA SEÇÃO ESTAVA FALTANDO:
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        # ESTA SEÇÃO ESTAVA FALTANDO:
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # 'add_fieldsets' é para a TELA DE CRIAÇÃO de um novo usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # Corrigido para 'password' e 'password2' como o UserAdmin espera
            'fields': ('email', 'password', 'password2', 'first_name', 'last_name')
        }),
    )

#admin.site.register(Eixo)
@admin.register(Eixo)
class EixoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

#admin.site.register(Polo)
@admin.register(Polo)
class PoloAdmin(admin.ModelAdmin):
    list_display = ('nome','drp',)
    list_filter = ('drp',)
    search_fields = ('nome','drp')
    autocomplete_fields = ('drp',)

#admin.site.register(ProjetoIntegrador)
@admin.register(ProjetoIntegrador)
class ProjetoIntegradorAdmin(admin.ModelAdmin):
    list_display = ('numero',)
    search_fields = ('numero',)

#admin.site.register(DRP)
@admin.register(DRP)
class DRPAdmin(admin.ModelAdmin):
    list_display = ('numero',)
    search_fields = ('numero',)

#admin.site.register(Curso)
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome','eixo',)
    search_fields = ('nome','eixo')
    list_filer = ('eixo',)
    autocomplete_fields = ['eixo',]

#admin.site.register(Tags)
@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Criar uma visualizacao melhor para o UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    inlines = (UserTagsInline, )
    list_display =  ('user', 'curso', 'polo', 'projeto_integrador')
    search_fields = ('user__email', 'curso__polo', 'polo__name')
    #autocomplete_fields = ['user', 'projeto_integrador', 'curso', 'polo', 'drp']

#admin.site.register(ProjectGroup)
@admin.register(ProjectGroup)
class ProjectGroupAdmin(admin.ModelAdmin):
    inlines = (ProjectGroupTagsInline, MembershipInline, JoinRequestInline, )
    list_display = ('name', 'projeto_integrador', 'creator', 'moderated', 'description')
    list_filter = ('projeto_integrador', 'drp', 'eixo', 'moderated')
    search_fields = ('name', 'description', 'creator__email')

#admin.site.register(Membership)
@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'project_group', 'role', 'date_joined')
    search_fields = ('user__email', 'project_group__name')

#admin.site.register(JoinRequest)
@admin.register(JoinRequest)
class JoinRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'project_group', 'status', 'date_requested')
    list_filter = ('status',)
    search_fields = ('user__email', 'project_group__name')

#admin.site.register(UserTags)
@admin.register(UserTags)
class UserTagsAdmin(admin.ModelAdmin):
    list_display = ('profile', 'tag',)
    search_fields = ('profile__user__email', 'tag__name')

#admin.site.register(ProjectGroupTags)
@admin.register(ProjectGroupTags)
class ProjectGroupTagsAdmin(admin.ModelAdmin):
    list_display = ('project_group', 'tag',)
    search_fields = ('project_group__name', 'tag__name')

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'is_used')
    search_fields = ('user__email', 'code')
