
from django.urls import path, include
from .views import EixoListView, PoloListView, DRPListView, CursoListView, ProjetoIntegradorListView, TagsListView, \
    ProfileDetailsView, ProfileSelfView, UserTagsListView

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
    ]