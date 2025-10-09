# Deploy em Produção - GruPI API

## 🚀 Deployment com Docker + PostgreSQL

### Pré-requisitos
- Docker e Docker Compose instalados
- Domínio apontado para o servidor (api.grupi.pavops.net)
- Certificado SSL (via Traefik, Nginx ou Let's Encrypt)

### Passo a Passo

#### 1. Clonar o repositório
```bash
git clone <seu-repositorio>
cd GruPI-Project
```

#### 2. Configurar variáveis de ambiente

**Para PRODUÇÃO:**
```bash
cp .env.example .env
nano .env
```

**Para DESENVOLVIMENTO:**
```bash
cp .env.dev .env
nano .env
```

**Importante:** Altere as seguintes variáveis:
- `DJANGO_SECRET_KEY`: Gere uma chave segura
- `DJANGO_ALLOWED_HOSTS`: Adicione seu domínio
- `CORS_ALLOWED_ORIGINS`: Configure os domínios permitidos
- `DB_PASSWORD`: Use uma senha forte para o banco de dados

Para gerar uma SECRET_KEY segura:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 3. Build e iniciar os containers

**PRODUÇÃO:**
```bash
# Usando Makefile (Linux/Mac)
make deploy

# Ou manualmente
docker-compose up -d --build
```

**DESENVOLVIMENTO:**
```bash
# Usando Makefile (Linux/Mac)
make dev-deploy

# Ou manualmente
docker-compose -f docker-compose.dev.yml up -d --build
```

#### 4. Verificar logs
```bash
# Produção
make logs
# ou
docker-compose logs -f web

# Desenvolvimento
make dev-logs
# ou
docker-compose -f docker-compose.dev.yml logs -f web
```

#### 5. Acessar a aplicação

**PRODUÇÃO:**
- API: https://api.grupi.pavops.net
- Admin: https://api.grupi.pavops.net/admin
- Documentação: https://api.grupi.pavops.net/api/schema/swagger-ui/

**DESENVOLVIMENTO:**
- API: https://api.grupi-dev.pavops.net (ou http://localhost:8000)
- Admin: https://api.grupi-dev.pavops.net/admin
- Documentação: https://api.grupi-dev.pavops.net/api/schema/swagger-ui/

### Usuário Admin Padrão
- **Email**: admin@grupi.pavops.net
- **Senha**: changeme123

⚠️ **IMPORTANTE**: Altere a senha imediatamente após o primeiro login!

## 🗄️ PostgreSQL

O projeto agora usa **PostgreSQL** como banco de dados padrão em todos os ambientes.

### Características:
- ✅ PostgreSQL 16 Alpine (imagem leve)
- ✅ Persistência de dados via volumes
- ✅ Healthcheck automático
- ✅ Bancos separados para dev e prod

### Acessar o banco de dados:

```bash
# Produção
make db-shell
# ou
docker-compose exec db psql -U grupi_user -d grupi_db

# Desenvolvimento
make dev-db-shell
# ou
docker-compose -f docker-compose.dev.yml exec db psql -U grupi_user -d grupi_db_dev
```

### Backup e Restore:

```bash
# Backup do PostgreSQL (produção)
docker-compose exec db pg_dump -U grupi_user grupi_db > backup_db_$(date +%Y%m%d).sql

# Restore (produção)
cat backup_db.sql | docker-compose exec -T db psql -U grupi_user grupi_db

# Backup via Django (produção)
make backup

# Backup via Django (desenvolvimento)
make dev-backup
```

## 🔧 Comandos Úteis (com Makefile)

### Produção:
```bash
make help           # Ver todos os comandos
make build          # Build da imagem
make up             # Iniciar containers
make down           # Parar containers
make logs           # Ver logs
make shell          # Django shell
make migrate        # Executar migrações
make collectstatic  # Coletar estáticos
make backup         # Backup do DB
make db-shell       # PostgreSQL shell
```

### Desenvolvimento:
```bash
make dev-build      # Build da imagem
make dev-up         # Iniciar containers
make dev-down       # Parar containers
make dev-logs       # Ver logs
make dev-shell      # Django shell
make dev-migrate    # Executar migrações
make dev-backup     # Backup do DB
make dev-db-shell   # PostgreSQL shell
```

### Sem Makefile (Windows):

**Produção:**
```bash
docker-compose up -d --build           # Iniciar
docker-compose down                    # Parar
docker-compose logs -f web             # Ver logs
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py migrate
docker-compose exec db psql -U grupi_user -d grupi_db
```

**Desenvolvimento:**
```bash
docker-compose -f docker-compose.dev.yml up -d --build
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml logs -f web
docker-compose -f docker-compose.dev.yml exec web python manage.py shell
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate
docker-compose -f docker-compose.dev.yml exec db psql -U grupi_user -d grupi_db_dev
```

## 📦 Estrutura dos Ambientes

```
.
├── docker-compose.yml          # Produção
├── docker-compose.dev.yml      # Desenvolvimento
├── .env.example                # Template
├── .env.dev                    # Configurações de dev
├── .env                        # Configurações de prod (criar manualmente)
└── Dockerfile                  # Build único para ambos
```

## 🔒 Segurança

### Configurações obrigatórias para produção:
1. ✅ `DJANGO_ENV=prod`
2. ✅ `DEBUG=False` (automático quando DJANGO_ENV=prod)
3. ✅ `DJANGO_SECRET_KEY` único e seguro
4. ✅ `ALLOWED_HOSTS` configurado corretamente
5. ✅ `DB_PASSWORD` forte e única
6. ✅ HTTPS habilitado (SSL/TLS)
7. ✅ CORS e CSRF configurados adequadamente
8. ✅ Senhas fortes para admin e banco de dados

### Diferenças entre Ambientes:

| Configuração | Desenvolvimento | Produção |
|--------------|-----------------|----------|
| DEBUG | True | False |
| HTTPS | Opcional | Obrigatório |
| Domínio | api.grupi-dev.pavops.net | api.grupi.pavops.net |
| DB Nome | grupi_db_dev | grupi_db |
| Workers Gunicorn | 2 (com reload) | 4 |
| Logs | Debug | Info |
| Volume mount | Sim (hot-reload) | Não |

## 🌐 Migração de Dados

### De SQLite para PostgreSQL:

```bash
# 1. Fazer backup dos dados do SQLite
python manage.py dumpdata > data_backup.json

# 2. Configurar PostgreSQL
# Editar .env com as configurações do PostgreSQL

# 3. Executar migrações no PostgreSQL
docker-compose exec web python manage.py migrate

# 4. Importar dados
docker-compose exec web python manage.py loaddata data_backup.json
```

### Entre ambientes (dev -> prod):

```bash
# 1. Backup do dev
make dev-backup

# 2. Copiar para produção e importar
make restore FILE=backup_dev_20251009_120000.json
```

## 📝 Variáveis de Ambiente

### Obrigatórias:

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `DJANGO_ENV` | Ambiente (dev/prod) | `prod` |
| `DJANGO_SECRET_KEY` | Chave secreta Django | (gerar nova) |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos | `api.grupi.pavops.net` |
| `DB_PASSWORD` | Senha do PostgreSQL | (senha forte) |

### Opcionais (com defaults):

| Variável | Default | Descrição |
|----------|---------|-----------|
| `DB_NAME` | grupi_db | Nome do banco |
| `DB_USER` | grupi_user | Usuário do banco |
| `DB_HOST` | db | Host do PostgreSQL |
| `DB_PORT` | 5432 | Porta do PostgreSQL |

## 🔍 Troubleshooting

### Erro: Database connection refused
```bash
# Verificar se o PostgreSQL está rodando
docker-compose ps

# Ver logs do banco
docker-compose logs db

# Aguardar o healthcheck
# O web service só inicia após o DB estar saudável
```

### Erro: Could not connect to database
- Verifique as credenciais no .env
- Verifique se o container do DB está rodando
- Aguarde alguns segundos após `docker-compose up`

### Erro: Static files não carregam
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Resetar o banco de dados:
```bash
# CUIDADO: Isso apaga todos os dados!

# Desenvolvimento
make dev-clean
make dev-deploy

# Produção (fazer backup primeiro!)
make backup
make clean
make deploy
```

## 📞 Suporte

Para problemas ou dúvidas, entre em contato:
- Email: dev-grupi@pavops.net
