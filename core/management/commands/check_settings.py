# core/management/commands/check_settings.py
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = "Exibe as configurações de segurança e ambiente mais importantes."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("=" * 30))
        self.stdout.write(self.style.SUCCESS("  VERIFICANDO CONFIGURAÇÕES ATIVAS"))
        self.stdout.write(self.style.SUCCESS("=" * 30))

        # Verifica o ambiente
        env = getattr(settings, 'ENV', 'NÃO DEFINIDO')
        self.stdout.write(f"Ambiente (ENV): {self.style.WARNING(env)}")

        # Configurações de segurança
        self.stdout.write("\n--- Segurança ---")
        self.display_setting('DEBUG')
        self.display_setting('ALLOWED_HOSTS')
        self.display_setting('CSRF_TRUSTED_ORIGINS')
        self.display_setting('SESSION_COOKIE_SECURE')
        self.display_setting('CSRF_COOKIE_SECURE')
        self.display_setting('SECURE_SSL_REDIRECT')

        # Configurações de banco de dados e e-mail
        self.stdout.write("\n--- Serviços ---")
        self.display_setting('DATABASES', 'default.NAME')
        self.display_setting('EMAIL_BACKEND')

        self.stdout.write(self.style.SUCCESS("\nVerificação concluída."))

    def display_setting(self, setting_name, path=None):
        try:
            value = getattr(settings, setting_name)
            if path: # Para acessar chaves de dicionário, como em DATABASES
                keys = path.split('.')
                temp_val = value
                for key in keys:
                    temp_val = temp_val[key]
                value = temp_val
        except (AttributeError, KeyError):
            value = self.style.ERROR("NÃO ENCONTRADO")

        self.stdout.write(f"{setting_name}: {self.style.WARNING(value)}")