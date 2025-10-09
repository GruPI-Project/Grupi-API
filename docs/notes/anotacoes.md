# Instala todas as dependências necessárias do projeto para que ele funcione:

> pip install -r requirements.txt

# Cria/ atualiza as dependências do projeto (se adicionar mais dependências é necessário executar novamente)

> pip freeze > requirements.txt

# Cria arquivos de migração baseados nas mudanças que fizemos nos códigos do app

> python manage.py makemigrations

# Aplica as migrações pendentes no banco de dados (no nosso caso, por enquanto é o SQLite)

> python manage.py migrate

# Roda o app (pelo ambiente Django)

> python manage.py runserver

# Executa o teste Automatizado (é preciso ter o arquivo __init__.py na pasta onde o teste está presente)

> python manage.py test core.tests.test_models

# Imprime as informações de teste do coverage no Terminal

> coverage report -m

# Gera o documento de teste do coverage em HTML

> coverage html

# Abre as informações do coverage no navegador

> start htmlcov\index.html