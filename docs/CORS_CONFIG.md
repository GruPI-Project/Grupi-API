# Configuração de CORS - GruPI API

## ✅ O que foi configurado

O projeto agora está configurado para aceitar requisições CORS (Cross-Origin Resource Sharing) do frontend React.

### 📦 Pacote Instalado
- **django-cors-headers** - Middleware para gerenciar headers CORS

### ⚙️ Configurações Aplicadas

#### 1. **Origens Permitidas**
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```
- Permite requisições do frontend React rodando em `localhost:3000` ou `127.0.0.1:3000`

#### 2. **Headers Permitidos**
- `authorization` - Para enviar tokens JWT
- `content-type` - Para enviar JSON
- `accept`, `origin`, `user-agent`, etc.

#### 3. **Métodos HTTP Permitidos**
- GET, POST, PUT, PATCH, DELETE, OPTIONS

#### 4. **Credenciais**
- `CORS_ALLOW_CREDENTIALS = True` - Permite envio de cookies e tokens de autenticação

## 🚀 Como Usar

### No Frontend React (axios ou fetch)

#### Exemplo com Axios:
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  withCredentials: true, // Importante para enviar cookies
  headers: {
    'Content-Type': 'application/json',
  }
});

// Login
const login = async (email, password) => {
  const response = await api.post('/auth/login/', {
    email,
    password
  });
  return response.data;
};

// Requisição autenticada
const getProfile = async (token) => {
  const response = await api.get('/profile/me/', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return response.data;
};
```

#### Exemplo com Fetch:
```javascript
// Login
const login = async (email, password) => {
  const response = await fetch('http://127.0.0.1:8000/api/v1/auth/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include', // Importante para cookies
    body: JSON.stringify({ email, password })
  });
  return await response.json();
};

// Requisição autenticada
const getProfile = async (token) => {
  const response = await fetch('http://127.0.0.1:8000/api/v1/profile/me/', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    credentials: 'include'
  });
  return await response.json();
};
```

## 🔒 Para Produção

Quando for para produção, atualize a configuração:

```python
# settings.py (produção)

# Adicione o domínio de produção
CORS_ALLOWED_ORIGINS = [
    "https://seu-frontend.com",
    "https://www.seu-frontend.com",
]

# OU use regex para subdomínios
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.seu-dominio\.com$",
]

# Não use CORS_ALLOW_ALL_ORIGINS = True em produção!
```

## 🐛 Troubleshooting

### Problema: Ainda aparece erro de CORS
**Solução:**
1. Certifique-se de que o servidor Django foi reiniciado após as mudanças
2. Limpe o cache do navegador
3. Verifique se a URL no frontend está correta (`http://127.0.0.1:8000` ou `http://localhost:8000`)

### Problema: Token JWT não está sendo enviado
**Solução:**
1. Certifique-se de incluir `Authorization: Bearer <token>` no header
2. Use `withCredentials: true` no axios ou `credentials: 'include'` no fetch

### Problema: Erro de preflight (OPTIONS)
**Solução:**
- O middleware CORS já trata automaticamente requisições OPTIONS
- Verifique se o `corsheaders.middleware.CorsMiddleware` está ANTES do `CommonMiddleware`

## 📝 Arquivos Modificados

- ✅ `GruPI/settings.py` - Adicionado `corsheaders` aos INSTALLED_APPS
- ✅ `GruPI/settings.py` - Adicionado `CorsMiddleware` ao MIDDLEWARE
- ✅ `GruPI/settings.py` - Adicionadas configurações CORS no final do arquivo

## 🎯 Próximos Passos

1. Reinicie o servidor Django
2. Teste as requisições do frontend React
3. Verifique no console do navegador se não há mais erros de CORS
4. Configure HTTPS em produção para maior segurança

---

**⚠️ Importante:** As configurações atuais são para DESENVOLVIMENTO. Em produção, restrinja as origens permitidas apenas aos domínios confiáveis!

