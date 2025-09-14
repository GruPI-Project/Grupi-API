# core/adapters.py

from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        Garante que, ao salvar, não tentemos lidar com o campo 'username'.
        """
        # O save padrão do allauth pode tentar acessar o username.
        # Ao sobrescrevermos e não chamarmos o método pai (`super().save_user...`),
        # garantimos que apenas os campos do nosso CustomUser sejam usados.
        user.save()
        return user