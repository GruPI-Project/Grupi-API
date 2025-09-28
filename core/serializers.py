# seu_app/serializers.py
from cProfile import Profile

from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import CustomUser, UserProfile, ProjetoIntegrador, DRP, Polo, Curso, Eixo, Tags, UserTags, ProjectGroup, \
    Membership
from django.db import transaction



#Serializers de Usuario e Profile
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id', 'name']

class CustomRegisterSerializer(RegisterSerializer):
    """
    Serializer personalizado para o registro de usuários, incluindo
    os campos obrigatórios do UserProfile.
    """

    # Removemos o campo username
    username = None

    projeto_integrador = serializers.PrimaryKeyRelatedField(queryset=ProjetoIntegrador.objects.all(), write_only=True)
    drp = serializers.PrimaryKeyRelatedField(queryset=DRP.objects.all(), write_only=True)
    polo = serializers.PrimaryKeyRelatedField(queryset=Polo.objects.all(), write_only=True)
    curso = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), write_only=True)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)


    def get_cleaned_data(self):
        # Pega os dados básicos (email, password, etc.) da classe pai
        data = super().get_cleaned_data()
        # Adiciona os novos campos de perfil aos dados que serão usados para criar o usuário
        data.update({
            'projeto_integrador': self.validated_data.get('projeto_integrador', ''),
            'drp': self.validated_data.get('drp', ''),
            'polo': self.validated_data.get('polo', ''),
            'curso': self.validated_data.get('curso', ''),
        })
        return data

    @transaction.atomic
    def save(self, request):
        user = CustomUser.objects.create_user(
            email=self.validated_data.get('email'),
            password=self.validated_data.get('password1'),
            first_name=self.validated_data.get('first_name', ''),
            last_name=self.validated_data.get('last_name', ''),
        )
        UserProfile.objects.create(
            user=user,
            projeto_integrador=self.validated_data.get('projeto_integrador'),
            polo=self.validated_data.get('polo'),
            curso=self.validated_data.get('curso'),
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para exibir os detalhes do perfil do usuário.
    Usa StringRelatedField para mostrar os nomes em vez dos IDs.
    """

    polo = serializers.StringRelatedField()
    curso = serializers.StringRelatedField()
    projeto_integrador = serializers.StringRelatedField()

    eixo = serializers.SerializerMethodField()
    drp = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        # Lista dos campos do UserProfile que você quer exibir
        fields = ['polo', 'curso', 'projeto_integrador', 'eixo', 'drp']

    def get_drp(self, obj):
        # Acessamos a drp através do polo do perfil
        if obj.polo:
            return obj.polo.drp.__str__() # Usamos __str__ para retornar o nome formatado
        return None

    def get_eixo(self, obj):
        """
        Este método retorna o Eixo.
        """
        # Acessamos o eixo através do curso do perfil
        if obj.curso:
            return obj.curso.eixo.nome
        return None

class CustomUserDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer para o endpoint /api/auth/user/.
    Define quais campos do usuário são retornados.
    """
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('pk', 'email', 'first_name', 'last_name', 'profile')

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('pk', 'email', 'first_name', 'last_name')

class UserProfileDetailSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    polo = serializers.StringRelatedField()
    curso = serializers.StringRelatedField()
    projeto_integrador = serializers.StringRelatedField()
    eixo = serializers.SerializerMethodField()
    drp = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id','user', 'polo', 'curso', 'projeto_integrador', 'eixo', 'drp', 'tags']

    def get_drp(self, obj):
        # Acessamos a drp através do polo do perfil
        if obj.polo:
            return obj.polo.drp.__str__()  # Usamos __str__ para retornar o nome formatado
        return None
    def get_eixo(self, obj):
        """
        Este método retorna o Eixo.
        """
        # Acessamos o eixo através do curso do perfil
        if obj.curso:
            return obj.curso.eixo.nome
        return None

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    polo = serializers.PrimaryKeyRelatedField(queryset=Polo.objects.all())
    curso = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all())
    projeto_integrador = serializers.PrimaryKeyRelatedField(queryset=ProjetoIntegrador.objects.all())
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(),
        many=True,
    )

    class Meta:
        model = UserProfile
        fields = ['polo', 'curso', 'projeto_integrador', 'tags']

#Serializers de informacoes base
class EixoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eixo
        fields = ['id', 'nome']

class DRPSerializer(serializers.ModelSerializer):
    class Meta:
        model = DRP
        fields = ['id', 'numero', 'nome']

class PoloSerializer(serializers.ModelSerializer):
    drp = DRPSerializer(read_only=True)

    class Meta:
        model = Polo
        fields = ['id', 'nome', 'drp']

class CursoSerializer(serializers.ModelSerializer):
    eixo = EixoSerializer(read_only=True)

    class Meta:
        model = Curso
        fields = ['id', 'nome', 'eixo']

class ProjetoIntegradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjetoIntegrador
        fields = ['id', 'numero']


#PROJECT-GROUPS
class MembershipSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Membership

        fields = ['user', 'role']

    def get_user(self, obj):
        if obj.user:
            return obj.user.email

class MembershipUserIdSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Membership
        fields = ['user','user_id', 'role']

    def get_user(self, obj):
        if obj.user:
            return obj.user.email

class ProjectGroupSerializer(serializers.ModelSerializer):

    creator = serializers.ReadOnlyField(source='creator.email')
    projeto_integrador = serializers.CharField(read_only=True)
    drp = serializers.CharField(read_only=True)
    polo = serializers.CharField(read_only=True)
    eixo = serializers.StringRelatedField(read_only=True)
    curso = serializers.StringRelatedField(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tags.objects.all(),
        allow_empty=True
    )
    #memberships = serializers.SerializerMethodField(read_only=True)
    memberships = MembershipSerializer(many=True, read_only=True)

    # def get_memberships(self, obj):
    #     return [membership.user.email for membership in obj.memberships.all()]

    class Meta:
        model = ProjectGroup
        fields = [
            'id',
            'name',
            'description',
            'creator',
            'projeto_integrador',
            'drp',
            'polo',
            'eixo',
            'curso',
            'moderated',
            'tags',
            'memberships'
        ]

    def validate_tags(self, value):
        if len(value) > 5:
            raise serializers.ValidationError("Não é possível associar mais de 5 tags a um grupo.")
        return value

class ProjectGroupUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(),
        many=True,
    )

    class Meta:
        model = ProjectGroup
        fields = ['name', 'description','tags']

class ProjectGroupMembersUserIdSerializer(serializers.ModelSerializer):
    memberships = MembershipUserIdSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectGroup
        fields = ['memberships']
