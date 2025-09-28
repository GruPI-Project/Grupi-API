
from rest_framework import permissions
from .models import Membership

class IsAdminOfGroup(permissions.BasePermission):
    """
    Permissão customizada para permitir que apenas os administradores de um grupo
    possam editar ou deletar o grupo.
    """
    message = 'Apenas o administrador do grupo pode realizar esta ação.'

    def has_object_permission(self, request, view, obj):
        """
        Verifica a permissão em nível de objeto.
        'obj' aqui é a instância de ProjectGroup.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            membership = Membership.objects.get(user=request.user, project_group=obj)
        except Membership.DoesNotExist:
            return False

        return membership.role == Membership.Role.ADMIN


from rest_framework import permissions
from .models import Membership


class CanRemoveMembership(permissions.BasePermission):
    """
    Permissão customizada para remover um membro de um grupo, com as seguintes regras:
    - O administrador do grupo pode remover qualquer outro membro.
    - Um membro pode sair do grupo (se remover).
    - O administrador do grupo NUNCA pode sair/ser removido.
    """
    message = 'Você não tem permissão para realizar esta ação.'

    def has_object_permission(self, request, view, obj):
        requesting_user = request.user
        membership_to_delete = obj
        group = membership_to_delete.project_group
        group_admin = group.creator

        if membership_to_delete.user == group_admin:
            self.message = 'O administrador não pode ser removido ou sair do grupo. O grupo deve ser deletado.'
            return False

        if requesting_user == membership_to_delete.user:
            return True

        if requesting_user == group_admin:
            return True

        self.message = 'Apenas o administrador do grupo pode remover outros membros.'
        return False