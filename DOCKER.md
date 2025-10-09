# Docker - GruPI API

Este guia fornece instruções rápidas para executar a aplicação GruPI usando Docker.

## 🚀 Quick Start

### Desenvolvimento Local

```bash
# 1. Copiar arquivo de exemplo de variáveis
cp .env.example .env

# 2. Editar .env e configurar as variáveis
nano .env

# 3. Iniciar aplicação
docker-compose up -d

# 4. Acessar
# API: http://localhost:8000
# Admin: http://localhost:8000/admin
# Docs: http://localhost:8000/api/schema/swagger-ui/
```

### Produção

```bash
# 1. Configurar variáveis de ambiente
cp .env.example .env
nano .env  # Configure com valores de produção

# 2. Gerar SECRET_KEY segura
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 3. Build e Deploy
make prod

# Ou manualmente:
docker-compose up -d --build
```

## 📋 Variáveis de Ambiente Obrigatórias

```env
DJANGO_ENV=prod
DJANGO_SECRET_KEY=sua-chave-secreta-aqui
DJANGO_ALLOWED_HOSTS=api.grupi.pavops.net
CORS_ALLOWED_ORIGINS=https://grupi.pavops.net
```

## 🛠️ Comandos Úteis

Com Makefile (Linux/Mac):
```bash
make help          # Ver todos os comandos
make up            # Iniciar
make down          # Parar
make logs          # Ver logs
make shell         # Django shell
make migrate       # Executar migrações
make backup        # Backup do DB
```

Sem Makefile (Windows):
```bash
docker-compose up -d              # Iniciar
docker-compose down               # Parar
docker-compose logs -f web        # Ver logs
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py migrate
```

## 📦 Estrutura

```
.
├── Dockerfile              # Imagem Docker
├── docker-compose.yml      # Orquestração
├── docker-entrypoint.sh    # Script de inicialização
├── nginx.conf              # Configuração Nginx (opcional)
├── .env.example            # Exemplo de variáveis
└── DEPLOYMENT.md           # Guia completo de deploy
```

## 🔒 Segurança

- ✅ SSL/TLS obrigatório em produção
- ✅ SECRET_KEY única e forte
- ✅ DEBUG=False em produção
- ✅ ALLOWED_HOSTS configurado
- ✅ CORS restrito

## 📚 Documentação Completa

Veja [DEPLOYMENT.md](DEPLOYMENT.md) para instruções detalhadas de deployment.

