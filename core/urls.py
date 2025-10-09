
from django.urls import path
from .views import EixoListView, PoloListView, DRPListView, CursoListView, ProjetoIntegradorListView, TagsListView, \
    ProfileDetailsView, ProfileSelfView, UserTagsListView, ProjectGroupView, ProjectGroupDetailView, \
    MembershipDeleteView, ProjectGroupSelfView, LeaveGroupView, JoinGroupView, ProjectGroupMembersListView, \
    JoinRequestListView, JoinRequestApproveView, JoinRequestRejectView, JoinRequestSelfView

app_name = 'core'

urlpatterns = [
    # --- Listas de Consulta ---
    path('eixos/', EixoListView.as_view(), name='eixo-list'),
    path('polos/', PoloListView.as_view(), name='polo-list'),
    path('drps/', DRPListView.as_view(), name='drp-list'),
    path('cursos/', CursoListView.as_view(), name='curso-list'),
    path('pis/', ProjetoIntegradorListView.as_view(), name='pi-list'),
    path('tags/', TagsListView.as_view(), name='tag-list'),

    # --- Perfis de Usuário (Recurso: 'profiles') ---
    path('profiles/me/', ProfileSelfView.as_view(), name='profile-me'),
    path('profiles/me/tags/', UserTagsListView.as_view(), name='profile-me-tags'),
    path('profiles/<uuid:user_pk>/', ProfileDetailsView.as_view(), name='profile-detail'),
    # <-- 'user' mudado para 'user_pk' por clareza

    # --- Grupos de Projeto (Recurso: 'project-groups') ---
    path('project-groups/', ProjectGroupView.as_view(), name='project-group-list-create'),
    path('project-groups/me/', ProjectGroupSelfView.as_view(), name='project-group-me'),
    path('project-groups/<int:pk>/', ProjectGroupDetailView.as_view(), name='project-group-detail'),
    path('project-groups/<int:pk>/join/', JoinGroupView.as_view(), name='project-group-join'),

    # --- Membros (Aninhado sob 'project-groups') ---
    path('project-groups/<int:group_pk>/members/', ProjectGroupMembersListView.as_view(), name='project-group-member-list'),
    path('project-groups/<int:group_pk>/members/<uuid:user_pk>/', MembershipDeleteView.as_view(), name='project-group-member-delete'),

    # --- Pedidos de Entrada (Recurso: 'join-requests') ---
    path('join-requests/', JoinRequestListView.as_view(), name='join-request-list'),
    path('join-requests/me/', JoinRequestSelfView.as_view(), name='join-request-me'),
    path('join-requests/<int:pk>/approve/', JoinRequestApproveView.as_view(), name='join-request-approve'),
    path('join-requests/<int:pk>/reject/', JoinRequestRejectView.as_view(), name='join-request-reject'),

    # --- Ações de Nível Superior ---
    path('leave-group/', LeaveGroupView.as_view(), name='leave-group'),
]