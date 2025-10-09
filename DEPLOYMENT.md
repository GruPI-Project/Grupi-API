# Deploy em Produção - GruPI API

## 🚀 Deployment com Docker

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
```bash
cp .env.example .env
nano .env
```

**Importante:** Altere as seguintes variáveis:
- `DJANGO_SECRET_KEY`: Gere uma chave segura
- `DJANGO_ALLOWED_HOSTS`: Adicione seu domínio
- `CORS_ALLOWED_ORIGINS`: Configure os domínios permitidos

Para gerar uma SECRET_KEY segura:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 3. Build e iniciar o container
```bash
docker-compose up -d --build
```

#### 4. Verificar logs
```bash
docker-compose logs -f web
```

#### 5. Acessar a aplicação
- API: https://api.grupi.pavops.net
- Admin: https://api.grupi.pavops.net/admin
- Documentação: https://api.grupi.pavops.net/api/schema/swagger-ui/

### Usuário Admin Padrão
- **Email**: admin@grupi.pavops.net
- **Senha**: changeme123

⚠️ **IMPORTANTE**: Altere a senha imediatamente após o primeiro login!

## 🔧 Configuração com Nginx (Opcional)

Se você estiver usando Nginx como proxy reverso, use a configuração em `nginx.conf`.

```bash
# Copiar configuração do nginx
sudo cp nginx.conf /etc/nginx/sites-available/grupi-api
sudo ln -s /etc/nginx/sites-available/grupi-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 📊 Comandos Úteis

### Executar migrações
```bash
docker-compose exec web python manage.py migrate
```

### Criar superusuário
```bash
docker-compose exec web python manage.py createsuperuser
```

### Coletar arquivos estáticos
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Acessar shell do Django
```bash
docker-compose exec web python manage.py shell
```

### Backup do banco de dados
```bash
docker-compose exec web python manage.py dumpdata > backup.json
```

### Restaurar backup
```bash
docker-compose exec web python manage.py loaddata backup.json
```

### Ver logs em tempo real
```bash
docker-compose logs -f web
```

### Reiniciar aplicação
```bash
docker-compose restart web
```

### Parar aplicação
```bash
docker-compose down
```

### Atualizar aplicação
```bash
git pull
docker-compose down
docker-compose up -d --build
```

## 🔒 Segurança

### Configurações obrigatórias para produção:
1. ✅ `DJANGO_ENV=prod` (já configurado)
2. ✅ `DEBUG=False` (ativado quando DJANGO_ENV=prod)
3. ✅ `DJANGO_SECRET_KEY` único e seguro
4. ✅ `ALLOWED_HOSTS` configurado corretamente
5. ✅ HTTPS habilitado (SSL/TLS)
6. ✅ CORS configurado adequadamente
7. ✅ Senhas fortes para admin

### Recomendações adicionais:
- Use um banco de dados PostgreSQL em produção (veja seção abaixo)
- Configure backups automáticos
- Monitore logs regularmente
- Mantenha as dependências atualizadas
- Use um gerenciador de secrets (AWS Secrets Manager, Vault, etc.)

## 🗄️ Migração para PostgreSQL (Recomendado para Produção)

### 1. Atualizar docker-compose.yml
```yaml
services:
  db:
    image: postgres:15-alpine
    container_name: grupi-db
    restart: unless-stopped
    environment:
      - POSTGRES_DB=grupi_db
      - POSTGRES_USER=grupi_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    depends_on:
      - db
    environment:
      - DB_ENGINE=django.db.backends.postgresql
      - DB_NAME=grupi_db
      - DB_USER=grupi_user
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_HOST=db
      - DB_PORT=5432

volumes:
  postgres_data:
```

### 2. Atualizar settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', ''),
    }
}
```

### 3. Adicionar psycopg2 ao requirements.txt
```
psycopg2-binary==2.9.9
```

## 📝 Variáveis de Ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `DJANGO_ENV` | `dev` | Ambiente (dev/prod) |
| `DJANGO_SECRET_KEY` | (inseguro) | Chave secreta do Django |
| `DJANGO_ALLOWED_HOSTS` | `*` | Hosts permitidos |
| `CORS_ALLOWED_ORIGINS` | localhost | Origens CORS permitidas |
| `DB_ENGINE` | sqlite3 | Engine do banco de dados |
| `DB_NAME` | db.sqlite3 | Nome do banco |
| `DB_USER` | - | Usuário do banco |
| `DB_PASSWORD` | - | Senha do banco |
| `DB_HOST` | - | Host do banco |
| `DB_PORT` | - | Porta do banco |

## 🔍 Troubleshooting

### Erro: Bad Gateway 502
- Verifique se o container está rodando: `docker-compose ps`
- Verifique os logs: `docker-compose logs web`
- Verifique se a porta 8000 está exposta

### Erro: Static files não carregam
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Erro: CSRF verification failed
- Verifique se `ALLOWED_HOSTS` inclui seu domínio
- Verifique configurações CORS

### Erro: Database locked
- Considere migrar para PostgreSQL
- Ou aumente o timeout do SQLite

## 📞 Suporte

Para problemas ou dúvidas, entre em contato:
- Email: dev-grupi@pavops.net

