from django.test import TestCase
from django.contrib import admin
from core import admin as core_admin
from core.models import (
    CustomUser, Eixo, Polo, ProjetoIntegrador, DRP, Curso, Tags,
    UserProfile, ProjectGroup, Membership, JoinRequest, UserTags, ProjectGroupTags
)

class AdminRegistrationTests(TestCase):
    def test_models_registered_in_admin(self):
        # Verifica se os modelos estão registrados
        models = [
            CustomUser, Eixo, Polo, ProjetoIntegrador, DRP, Curso, Tags,
            UserProfile, ProjectGroup, Membership, JoinRequest, UserTags, ProjectGroupTags
        ]
        for model in models:
            with self.subTest(model=model):
                self.assertIn(model, admin.site._registry)

    def test_custom_user_admin_inlines(self):
        model_admin = admin.site._registry[CustomUser]
        self.assertTrue(any(isinstance(inline, type) and inline.__name__ == 'UserProfileInline'
                            for inline in model_admin.inlines))

    def test_userprofile_admin_inlines(self):
        model_admin = admin.site._registry[UserProfile]
        self.assertTrue(any(isinstance(inline, type) and inline.__name__ == 'UserTagsInline'
                            for inline in model_admin.inlines))

    def test_projectgroup_admin_inlines(self):
        model_admin = admin.site._registry[ProjectGroup]
        inline_names = [inline.__name__ for inline in model_admin.inlines]
        self.assertIn('ProjectGroupTagsInline', inline_names)
        self.assertIn('MembershipInline', inline_names)
        self.assertIn('JoinRequestInline', inline_names)

    def test_customuser_admin_list_display(self):
        model_admin = admin.site._registry[CustomUser]
        self.assertIn('email', model_admin.list_display)
        self.assertIn('is_staff', model_admin.list_display)

    def test_projectgroup_admin_search_fields(self):
        model_admin = admin.site._registry[ProjectGroup]
        self.assertIn('name', model_admin.search_fields)
        self.assertIn('creator__email', model_admin.search_fields)

    def test_membership_admin_list_display(self):
        model_admin = admin.site._registry[Membership]
        self.assertIn('user', model_admin.list_display)
        self.assertIn('role', model_admin.list_display)

    def test_joinsolicitacao_admin_list_filter(self):
        model_admin = admin.site._registry[JoinRequest]
        self.assertIn('status', model_admin.list_filter)
