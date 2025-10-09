.PHONY: help build up down restart logs shell migrate makemigrations collectstatic createsuperuser test clean

help: ## Mostrar esta ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build da imagem Docker
	docker-compose build

up: ## Iniciar containers
	docker-compose up -d

down: ## Parar containers
	docker-compose down

restart: ## Reiniciar containers
	docker-compose restart

logs: ## Ver logs em tempo real
	docker-compose logs -f web

shell: ## Acessar shell do Django
	docker-compose exec web python manage.py shell

bash: ## Acessar bash do container
	docker-compose exec web bash

migrate: ## Executar migrações
	docker-compose exec web python manage.py migrate

makemigrations: ## Criar novas migrações
	docker-compose exec web python manage.py makemigrations

collectstatic: ## Coletar arquivos estáticos
	docker-compose exec web python manage.py collectstatic --noinput

createsuperuser: ## Criar superusuário
	docker-compose exec web python manage.py createsuperuser

backup: ## Fazer backup do banco de dados
	docker-compose exec web python manage.py dumpdata > backup_$(shell date +%Y%m%d_%H%M%S).json

restore: ## Restaurar backup (use: make restore FILE=backup.json)
	docker-compose exec web python manage.py loaddata $(FILE)

clean: ## Limpar containers, volumes e imagens
	docker-compose down -v
	docker system prune -f

deploy: ## Deploy completo (build + up + migrate + collectstatic)
	make build
	make up
	sleep 5
	make migrate
	make collectstatic
	@echo "Deploy concluído!"

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

