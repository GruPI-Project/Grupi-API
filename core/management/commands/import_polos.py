import json
from django.core.management.base import BaseCommand
from core.models import Polo, DRP

class Command(BaseCommand):
    help = "Importa polos e DRPs do arquivo polos.json"

    def handle(self, *args, **kwargs):
        with open(r'/data/polos.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for entry in data:
            polo_name = entry['name'].strip()
            drp_str = entry['drp'].strip()

            # Ignora cabeçalhos inválidos
            if polo_name.upper() == "POLO" or drp_str.upper() == "DRP":
                continue

            try:
                # Extrai o número do tipo "DRP01" → 1
                drp_num = int(drp_str.replace("DRP", ""))
            except ValueError:
                self.stdout.write(self.style.WARNING(f'DRP inválido para o polo {polo_name}: {drp_str}'))
                continue

            # Cria ou busca DRP com número
            drp, created_drp = DRP.objects.get_or_create(numero=drp_num)

            # Cria ou busca Polo com DRP relacionado
            polo, created_polo = Polo.objects.get_or_create(nome=polo_name, drp=drp)

            if created_polo:
                self.stdout.write(self.style.SUCCESS(f'Criado polo {polo_name} com DRP {drp_str}'))
            else:
                self.stdout.write(f'Polo {polo_name} já existe.')

        self.stdout.write(self.style.SUCCESS('Importação finalizada.'))
