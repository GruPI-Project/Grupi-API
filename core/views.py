from django.template.defaulttags import querystring
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Eixo, Polo, DRP, Curso, ProjetoIntegrador, Tags, UserProfile, UserTags
from .serializers import EixoSerializer, PoloSerializer, DRPSerializer, CursoSerializer, ProjetoIntegradorSerializer, \
    TagSerializer, UserProfileSerializer, UserProfileDetailSerializer, UserProfileUpdateSerializer


class EixoListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Eixo.objects.all()
    serializer_class = EixoSerializer

class PoloListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Polo.objects.all()
    serializer_class = PoloSerializer

class DRPListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DRP.objects.all()
    serializer_class = DRPSerializer

class CursoListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class ProjetoIntegradorListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ProjetoIntegrador.objects.all()
    serializer_class = ProjetoIntegradorSerializer

class TagsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Tags.objects.all()
    serializer_class = TagSerializer

class ProfileSelfView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileDetailSerializer

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UserProfileUpdateSerializer
        return UserProfileDetailSerializer

    def get_object(self):
        return self.request.user.profile

class ProfileDetailsView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer
    lookup_field = 'user'

class UserTagsListView(generics.ListAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = self.request.user.profile
        return profile.tags.all()