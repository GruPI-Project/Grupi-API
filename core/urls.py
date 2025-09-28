
from django.urls import path, include
from .views import EixoListView, PoloListView, DRPListView, CursoListView, ProjetoIntegradorListView, TagsListView, \
    ProfileDetailsView, ProfileSelfView, UserTagsListView, ProjectGroupView, ProjectGroupDetailView, \
    ProjectGroupMembersView, MembershipDeleteView, ProjectGroupSelfView, LeaveGroupView

# app_name é uma boa prática para organizar as URLs e evitar conflitos de nomes
app_name = 'core'


urlpatterns = [
    path('eixos/', EixoListView.as_view(), name='eixo-list'),
    path('polos/', PoloListView.as_view(), name='polo-list'),
    path('drps/', DRPListView.as_view(), name='drp-list'),
    path('cursos/', CursoListView.as_view(), name='curso-list'),
    path('pis/', ProjetoIntegradorListView.as_view(), name='projeto-integradores-list'),
    path('tags/', TagsListView.as_view(), name='tags-list'),
    path('profile/<uuid:user>/', ProfileDetailsView.as_view(), name='profile'),
    path('profile/me/', ProfileSelfView.as_view(), name='profile-me'),
    path('profile/me/tags/', UserTagsListView.as_view(), name='profile-me-tags'),
    path('project-groups/', ProjectGroupView.as_view(), name='project-group-list'),
    path('project-groups/me/', ProjectGroupSelfView.as_view(), name='project-group-self'),
    path('project-groups/leave/',LeaveGroupView.as_view(), name='project-group-leave'),
    path('project-groups/<int:pk>/', ProjectGroupDetailView.as_view(), name='project-group'),
    path('project-groups/<int:pk>/members/', ProjectGroupMembersView.as_view(), name='project-group-members'),
    path('project-groups/<int:group_pk>/members/<uuid:user_pk>/', MembershipDeleteView.as_view(), name='group-member-delete'),
]