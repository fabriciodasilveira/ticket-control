# Guia de Implantação para Testes

Este guia explica como implantar o sistema de gerenciamento de tarefas para testes locais.

## Pré-requisitos

Certifique-se de ter instalado:

- **Docker** (versão 20.10+)
- **Docker Compose** (versão 2.0+)
- **Git**

### Verificar instalações

```bash
docker --version
docker-compose --version
git --version
```

## Opção 1: Implantação Rápida (Recomendada para Testes)

Esta opção sobe apenas o banco de dados, Redis e Backend API para testes rápidos.

### Passo 1: Clonar e acessar o diretório

```bash
cd /workspace/infrastructure
```

### Passo 2: Criar arquivo .env

```bash
cp .env.example .env
```

Edite o `.env` se necessário (opcional para testes locais).

### Passo 3: Iniciar os serviços

```bash
# Inicia PostgreSQL, Redis e Backend
docker-compose up -d postgres redis backend
```

### Passo 4: Verificar se os serviços estão rodando

```bash
docker-compose ps
```

### Passo 5: Acessar a API

A API estará disponível em: http://localhost:8003

- **Swagger UI**: http://localhost:8003/docs
- **ReDoc**: http://localhost:8003/redoc
- **Health Check**: http://localhost:8003/health

### Passo 6: Criar usuário Admin inicial

```bash
# Executar script para criar admin
docker-compose exec backend python -c "
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()

admin = User(
    email='admin@taskmanager.com',
    password_hash=get_password_hash('Admin@123'),
    full_name='Administrador Geral',
    role='admin'
)

db.add(admin)
db.commit()
db.close()

print('Usuário admin criado com sucesso!')
print('Email: admin@taskmanager.com')
print('Senha: Admin@123')
"
```

## Opção 2: Implantação Completa (Backend + Frontend)

### Passo 1: Iniciar todos os serviços

```bash
cd /workspace/infrastructure
docker-compose up -d
```

Isso iniciará:
- PostgreSQL (porta 5434)
- Redis (porta 6381)
- Backend API (porta 8003)
- Frontend Web (porta 3001)

### Passo 2: Aguardar build e inicialização

O primeiro build pode levar alguns minutos. Monitore os logs:

```bash
docker-compose logs -f
```

### Passo 3: Acessar as aplicações

- **Frontend Web**: http://localhost:3001
- **Backend API**: http://localhost:8003
- **Swagger UI**: http://localhost:8003/docs

## Opção 3: Modo Desenvolvimento (Com Hot Reload)

Para desenvolvimento ativo com recarregamento automático:

```bash
# Iniciar em modo development
docker-compose -f docker-compose.dev.yml up -d
```

## Comandos Úteis

### Ver logs em tempo real

```bash
# Todos os serviços
docker-compose logs -f

# Apenas backend
docker-compose logs -f backend

# Apenas frontend
docker-compose logs -f frontend

# Apenas banco de dados
docker-compose logs -f postgres
```

### Parar todos os serviços

```bash
docker-compose down
```

### Parar e remover volumes (limpeza completa)

```bash
docker-compose down -v
```

### Reiniciar um serviço específico

```bash
docker-compose restart backend
```

### Executar comandos dentro dos containers

```bash
# Acessar shell do backend
docker-compose exec backend bash

# Acessar psql do banco
docker-compose exec postgres psql -U postgres -d taskmanager

# Acessar redis-cli
docker-compose exec redis redis-cli
```

### Rodar migrações do banco

```bash
docker-compose exec backend alembic upgrade head
```

### Rodar testes

```bash
docker-compose exec backend pytest
```

## Estrutura de Portas

| Serviço | Porta Externa | URL | Conflito |
|---------|--------------|-----|----------|
| Frontend | 3001 | http://localhost:3001 | ✅ Não conflita (sistema usa 3000) |
| Backend API | 8003 | http://localhost:8003 | ✅ Não conflita (sistema usa 8000) |
| PostgreSQL | 5434 | localhost:5434 | ✅ Não conflita (sistema usa 5432) |
| Redis | 6381 | localhost:6381 | ✅ Não conflita (sistema usa 6379) |

## Credenciais de Teste

Após criar o usuário admin:

- **Email**: admin@taskmanager.com
- **Senha**: Admin@123

## Variáveis de Ambiente

O arquivo `.env` contém as configurações:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/taskmanager

# Redis
REDIS_URL=redis://redis:6379/0

# Segurança
SECRET_KEY=sua-chave-secreta-para-testes
DEBUG=true

# CORS
CORS_ORIGINS=["http://localhost:3001", "http://localhost:8080"]

# Cloudflare R2 (opcional para testes)
R2_ACCOUNT_ID=
R2_ACCESS_KEY_ID=
R2_SECRET_ACCESS_KEY=
R2_BUCKET_NAME=
R2_PUBLIC_URL=
```

## Troubleshooting

### Erro: "Port already in use"

Se alguma porta já estiver em uso:

```bash
# Verificar qual processo está usando a porta
lsof -i :8003
lsof -i :3001
lsof -i :5434
lsof -i :6381

# Matar o processo (cuidado!)
kill -9 <PID>

# Ou alterar as portas no docker-compose.yml
```

### Erro: "Container failed to start"

Verifique os logs:

```bash
docker-compose logs <nome-do-serviço>
```

Problemas comuns:
- Banco de dados não está pronto (aguarde o healthcheck)
- Variáveis de ambiente incorretas
- Permissões de volume

### Reset completo

Se algo der errado, faça um reset completo:

```bash
# Parar tudo e remover volumes
docker-compose down -v

# Remover imagens (opcional)
docker-compose rm -f

# Subir novamente
docker-compose up -d
```

## Próximos Passos

1. Acesse http://localhost:8003/docs para explorar a API
2. Crie usuários, cargos, setores e tarefas
3. Teste os endpoints de autenticação
4. Implemente o frontend ou mobile conforme necessário

## Mobile (React Native/Expo)

Para testar o aplicativo mobile:

```bash
cd /workspace/mobile

# Instalar dependências
npm install

# Iniciar Expo
npx expo start

# Escanear QR Code com app Expo Go (Android/iOS)
```

Configurar a URL da API no mobile para apontar para seu IP local (não localhost).

---

**Dúvidas?** Consulte a documentação completa em `/workspace/docs/`
