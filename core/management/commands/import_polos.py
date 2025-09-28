import json
import os
from django.core.management.base import BaseCommand
from core.models import Polo, DRP

class Command(BaseCommand):
    help = "Importa polos e DRPs do arquivo polos.json"

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            '-f',
            type=str,
            # É uma boa prática definir o default aqui.
            default=os.path.join('data', 'polos.json'),
            help='Caminho para o arquivo polos.json (padrão: data/polos.json)',
        )

    def handle(self, *args, **options):
        file_path = options['file']
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Arquivo não encontrado: {file_path}"))
            return
        for entry in data:
            polo_name = entry['name'].strip()
            drp_str = entry['drp'].strip()

            self.stdout.write(self.style.SUCCESS(f'Criando polo {polo_name} com DRP {drp_str}'))
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
            self.stdout.write(self.style.SUCCESS(f'Criado DRP: {drp_num}'))
            drp, created_drp = DRP.objects.get_or_create(numero=drp_num)

            # Cria ou busca Polo com DRP relacionado
            polo, created_polo = Polo.objects.get_or_create(nome=polo_name, drp=drp)

            if created_polo:
                self.stdout.write(self.style.SUCCESS(f'Criado polo {polo_name} com DRP {drp_str}'))
            else:
                self.stdout.write(f'Polo {polo_name} já existe.')

        self.stdout.write(self.style.SUCCESS('Importação finalizada.'))
