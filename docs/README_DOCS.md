# Documentação da API GruPI

## 📚 Como Acessar a Documentação

A documentação da API GruPI está disponível em três formatos diferentes:

### 1. **ReDoc** (Recomendado para leitura)
```
http://127.0.0.1:8000/api/redoc/
```
- Interface limpa e focada em documentação
- Melhor para ler e entender a API
- Três colunas: menu lateral, conteúdo central e exemplos à direita

### 2. **Swagger UI** (Recomendado para testar)
```
http://127.0.0.1:8000/api/docs/
```
- Interface interativa para testar endpoints
- Permite executar requisições diretamente do navegador
- Suporta autenticação via JWT
- Ideal para desenvolvimento e testes

### 3. **Schema OpenAPI (YAML/JSON)**
```
http://127.0.0.1:8000/api/schema/
http://127.0.0.1:8000/api/schema/?format=yaml
```
- Schema OpenAPI 3.0 bruto
- Use para gerar clientes automaticamente
- Compatível com ferramentas como Postman, Insomnia, etc.

## 🚀 Iniciar o Servidor

Para visualizar a documentação, primeiro inicie o servidor Django:

```bash
python manage.py runserver
```

## 🔑 Testando Endpoints Autenticados no Swagger UI

1. Acesse o Swagger UI em `http://127.0.0.1:8000/api/docs/`
2. Primeiro, faça login ou registre um usuário:
   - Use o endpoint `POST /auth/login/` ou `POST /auth/registration/`
   - Copie o token `access` da resposta
3. Clique no botão **"Authorize"** (cadeado) no topo da página
4. Cole o token no campo `bearerAuth` (não precisa adicionar "Bearer", apenas o token)
5. Clique em "Authorize" e depois "Close"
6. Agora você pode testar todos os endpoints autenticados!

## 📦 Arquivos de Documentação

- **`openapi.yaml`** - Documentação OpenAPI 3.0.3 completa escrita manualmente
- **Schema Auto-gerado** - O drf-spectacular também gera o schema automaticamente baseado nas views

## 🛠️ Tecnologias Utilizadas

- **drf-spectacular** - Geração automática de schema OpenAPI
- **drf-spectacular-sidecar** - Assets estáticos do Swagger UI e ReDoc
- **ReDoc** - Interface de documentação elegante e responsiva
- **Swagger UI** - Interface interativa para testar a API

## 📖 Estrutura da Documentação

A API está organizada em 4 categorias principais:

### 🔐 Autenticação
- Registro de usuários
- Login/Logout
- Refresh de tokens JWT
- Consulta de usuário autenticado

### 👤 Perfil de Usuário
- Visualizar e editar perfil próprio
- Consultar perfis de outros usuários
- Gerenciar tags de habilidades

### 👥 Grupos de Projeto
- Criar, listar, visualizar grupos
- Atualizar e deletar grupos (apenas admin)
- Gerenciar membros
- Sair de grupos

### 📚 Dados Acadêmicos
- Listar Eixos, Cursos, DRPs, Polos
- Listar Projetos Integradores (PI)
- Listar Tags disponíveis

## 🎯 Próximos Passos

1. Explore a documentação no ReDoc para entender a estrutura da API
2. Use o Swagger UI para testar os endpoints
3. Baixe o schema OpenAPI para importar em ferramentas como Postman
4. Compartilhe a URL da documentação com sua equipe!

---

**Dica:** Se você fez alterações nas views ou serializers, a documentação será atualizada automaticamente ao recarregar a página! 🔄

