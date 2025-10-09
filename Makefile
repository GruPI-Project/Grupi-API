.PHONY: help build up down restart logs shell migrate makemigrations collectstatic createsuperuser backup restore clean deploy prod dev-up dev-down dev-logs

help: ## Mostrar esta ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ==========================================
# PRODUÇÃO
# ==========================================

build: ## Build da imagem Docker (produção)
	docker-compose build

up: ## Iniciar containers (produção)
	docker-compose up -d

down: ## Parar containers (produção)
	docker-compose down

restart: ## Reiniciar containers (produção)
	docker-compose restart

logs: ## Ver logs em tempo real (produção)
	docker-compose logs -f web

# ==========================================
# DESENVOLVIMENTO
# ==========================================

dev-build: ## Build da imagem Docker (dev)
	docker-compose -f docker-compose.dev.yml build

dev-up: ## Iniciar containers (dev)
	docker-compose -f docker-compose.dev.yml up -d

dev-down: ## Parar containers (dev)
	docker-compose -f docker-compose.dev.yml down

dev-restart: ## Reiniciar containers (dev)
	docker-compose -f docker-compose.dev.yml restart

dev-logs: ## Ver logs em tempo real (dev)
	docker-compose -f docker-compose.dev.yml logs -f web

dev-shell: ## Acessar shell do Django (dev)
	docker-compose -f docker-compose.dev.yml exec web python manage.py shell

dev-bash: ## Acessar bash do container (dev)
	docker-compose -f docker-compose.dev.yml exec web bash

# ==========================================
# COMANDOS GERAIS
# ==========================================

shell: ## Acessar shell do Django (prod)
	docker-compose exec web python manage.py shell

bash: ## Acessar bash do container (prod)
	docker-compose exec web bash

migrate: ## Executar migrações (prod)
	docker-compose exec web python manage.py migrate

dev-migrate: ## Executar migrações (dev)
	docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

makemigrations: ## Criar novas migrações (prod)
	docker-compose exec web python manage.py makemigrations

dev-makemigrations: ## Criar novas migrações (dev)
	docker-compose -f docker-compose.dev.yml exec web python manage.py makemigrations

collectstatic: ## Coletar arquivos estáticos (prod)
	docker-compose exec web python manage.py collectstatic --noinput

dev-collectstatic: ## Coletar arquivos estáticos (dev)
	docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic --noinput

createsuperuser: ## Criar superusuário (prod)
	docker-compose exec web python manage.py createsuperuser

dev-createsuperuser: ## Criar superusuário (dev)
	docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser

backup: ## Fazer backup do banco de dados (prod)
	docker-compose exec web python manage.py dumpdata > backup_$(shell date +%Y%m%d_%H%M%S).json

dev-backup: ## Fazer backup do banco de dados (dev)
	docker-compose -f docker-compose.dev.yml exec web python manage.py dumpdata > backup_dev_$(shell date +%Y%m%d_%H%M%S).json

restore: ## Restaurar backup (prod - use: make restore FILE=backup.json)
	docker-compose exec web python manage.py loaddata $(FILE)

dev-restore: ## Restaurar backup (dev - use: make dev-restore FILE=backup.json)
	docker-compose -f docker-compose.dev.yml exec web python manage.py loaddata $(FILE)

db-shell: ## Acessar PostgreSQL shell (prod)
	docker-compose exec db psql -U grupi_user -d grupi_db

dev-db-shell: ## Acessar PostgreSQL shell (dev)
	docker-compose -f docker-compose.dev.yml exec db psql -U grupi_user -d grupi_db_dev

clean: ## Limpar containers, volumes e imagens (prod)
	docker-compose down -v
	docker system prune -f

dev-clean: ## Limpar containers, volumes e imagens (dev)
	docker-compose -f docker-compose.dev.yml down -v

deploy: ## Deploy completo (build + up + migrate + collectstatic) - PRODUÇÃO
	make build
	make up
	sleep 10
	make migrate
	make collectstatic
	@echo "Deploy em PRODUÇÃO concluído!"

dev-deploy: ## Deploy completo (build + up + migrate + collectstatic) - DEV
	make dev-build
	make dev-up
	sleep 10
	make dev-migrate
	make dev-collectstatic
	@echo "Deploy em DESENVOLVIMENTO concluído!"

prod: ## Deploy em produção
	@echo "Iniciando deploy em produção..."
	git pull
	make build
	make down
	make up
	sleep 10
	make migrate
	make collectstatic
	@echo "Deploy em produção concluído!"
