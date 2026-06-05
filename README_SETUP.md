# 🍔 TaskManager - Sistema de Gestão para Restaurantes

Sistema completo para gerenciamento de tarefas, checklists e auditorias operacionais de hamburguerias e restaurantes.

## 🚀 Implantação Rápida para Testes

### Método 1: Script Automático (Recomendado)

```bash
# Executar script de setup
./setup-test.sh
```

Este script irá:
- ✅ Verificar se Docker e Docker Compose estão instalados
- ✅ Iniciar PostgreSQL, Redis e Backend API
- ✅ Criar usuário administrador automaticamente
- ✅ Mostrar informações de acesso

### Método 2: Manual com Docker Compose

```bash
# 1. Acessar diretório de infraestrutura
cd infrastructure

# 2. Copiar arquivo de ambiente
cp .env.example .env

# 3. Iniciar serviços
docker-compose up -d postgres redis backend

# 4. Aguardar inicialização (cerca de 15 segundos)
sleep 15

# 5. Criar usuário admin
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
print('Admin criado!')
"
```

## 📍 Acessar o Sistema

Após a implantação:

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **API Backend** | http://localhost:8003 | API REST principal |
| **Swagger UI** | http://localhost:8003/docs | Documentação interativa da API |
| **ReDoc** | http://localhost:8003/redoc | Documentação alternativa |
| **Health Check** | http://localhost:8003/health | Status do serviço |
| **Frontend Web** | http://localhost:3001 | Interface web (se implantado) |
| **PostgreSQL** | localhost:5434 | Banco de dados |
| **Redis** | localhost:6381 | Cache |
| **Nginx (Produção)** | localhost:82 | Reverse proxy (perfil production) |

## 🔐 Credenciais de Administrador

```
Email: admin@taskmanager.com
Senha: Admin@123
```

## 🏗️ Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                      TaskManager SaaS                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Frontend   │  │    Mobile    │  │   API REST   │       │
│  │   Next.js    │  │ React Native │  │   FastAPI    │       │
│  │   :3001      │  │    Expo      │  │   :8003      │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                              │                               │
│                              ▼                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Backend Services                        │    │
│  │  • Autenticação JWT     • Tarefas & Checklists      │    │
│  │  • Upload de Imagens    • Relatórios                │    │
│  │  • Notificações         • Auditoria                 │    │
│  │  • QR Codes             • Dashboard                 │    │
│  └─────────────────────────────────────────────────────┘    │
│                              │                               │
│              ┌───────────────┴───────────────┐              │
│              ▼                               ▼              │
│  ┌─────────────────────┐      ┌─────────────────────┐      │
│  │   PostgreSQL :5434  │      │     Redis :6381     │      │
│  │   (Dados)           │      │   (Cache/Sessions)  │      │
│  └─────────────────────┘      └─────────────────────┘      │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 👥 Perfis de Usuário

### Administrador Geral
- Cadastrar/editar usuários, cargos, setores
- Criar tarefas, checklists, unidades
- Visualizar todos os relatórios
- Gerenciar permissões

### Gerente
- Visualizar funcionários da unidade
- Aprovar/reprovar tarefas
- Reatribuir tarefas
- Receber notificações

### Funcionário
- Visualizar tarefas atribuídas
- Executar tarefas com fotos
- Adicionar observações
- Visualizar histórico próprio

## 📋 Funcionalidades Principais

- ✅ Gestão de Tarefas (diárias, semanais, mensais)
- ✅ Checklists personalizáveis (Abertura, Fechamento, Limpeza)
- ✅ Evidências fotográficas com armazenamento Cloudflare R2
- ✅ Controle de temperatura (Freezers, Geladeiras)
- ✅ QR Codes por área (Cozinha, Estoque, Salão)
- ✅ Modo offline com sincronização
- ✅ Assinatura digital
- ✅ Geolocalização opcional
- ✅ Dashboard gerencial com indicadores
- ✅ Notificações (Push, Email)
- ✅ Auditoria completa e rastreabilidade
- ✅ Multiunidades/Lojas
- ✅ Relatórios em PDF, Excel, CSV

## 🛠️ Comandos Úteis

### Ver logs
```bash
cd infrastructure
docker-compose logs -f
```

### Ver logs de um serviço específico
```bash
docker-compose logs -f backend
docker-compose logs -f postgres
docker-compose logs -f redis
```

### Parar serviços
```bash
docker-compose down
```

### Reset completo (remove volumes)
```bash
docker-compose down -v
```

### Reiniciar backend
```bash
docker-compose restart backend
```

### Acessar terminal do backend
```bash
docker-compose exec backend bash
```

### Acessar banco de dados
```bash
docker-compose exec postgres psql -U postgres -d taskmanager
```

### Rodar migrações
```bash
docker-compose exec backend alembic upgrade head
```

### Rodar testes
```bash
docker-compose exec backend pytest
```

## 📁 Estrutura do Projeto

```
/workspace
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # Rotas da API
│   │   ├── core/           # Configurações e segurança
│   │   ├── db/             # Conexão com banco
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── schemas/        # Schemas Pydantic
│   │   └── services/       # Serviços de negócio
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # Next.js Web App
│   ├── src/app/
│   ├── src/components/
│   ├── Dockerfile
│   └── package.json
├── mobile/                 # React Native (Expo)
├── infrastructure/         # Docker Compose
│   ├── docker-compose.yml
│   ├── nginx/
│   └── .env.example
├── docs/                   # Documentação
├── setup-test.sh          # Script de setup
└── IMPLANTACAO_TESTE.md   # Guia detalhado
```

## 🔧 Variáveis de Ambiente

### Backend (.env)
```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/taskmanager
REDIS_URL=redis://redis:6379/0
SECRET_KEY=sua-chave-secreta
DEBUG=true
CORS_ORIGINS=["http://localhost:3000"]
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8003/api/v1
```

## 📊 Portas Utilizadas

| Serviço | Porta Externa | Porta Interna | Protocolo | Conflito com Sistema |
|---------|--------------|---------------|-----------|---------------------|
| Frontend | 3001 | 3000 | HTTP | ✅ Não conflita (sistema usa 3000) |
| Backend API | 8003 | 8000 | HTTP | ✅ Não conflita (sistema usa 8000) |
| PostgreSQL | 5434 | 5432 | TCP | ✅ Não conflita (sistema usa 5432) |
| Redis | 6381 | 6379 | TCP | ✅ Não conflita (sistema usa 6379) |
| Nginx HTTP (prod) | 82 | 80 | HTTP | ✅ Não conflita (sistema usa 80, 81) |
| Nginx HTTPS (prod) | 444 | 443 | HTTPS | ✅ Não conflita (sistema usa 9443) |

## 🧪 Testando a API

### Via Swagger UI
1. Acesse http://localhost:8003/docs
2. Clique em `/api/v1/auth/login`
3. Execute com:
   - username: `admin@taskmanager.com`
   - password: `Admin@123`
4. Use o token retornado nas demais requisições

### Via curl
```bash
# Login
curl -X POST http://localhost:8003/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@taskmanager.com&password=Admin@123"

# Listar usuários (requer token)
curl http://localhost:8003/api/v1/users \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 🚨 Troubleshooting

### Erro: "Port already in use"
```bash
# Verificar processo usando a porta
lsof -i :8003
lsof -i :3001
lsof -i :5434
lsof -i :6381

# Matar processo ou alterar portas no docker-compose.yml
```

### Erro: "Container failed to start"
```bash
# Ver logs detalhados
docker-compose logs <serviço>

# Verificar variáveis de ambiente
cat infrastructure/.env
```

### Banco de dados não conecta
```bash
# Reiniciar PostgreSQL
docker-compose restart postgres

# Aguardar healthcheck
docker-compose ps
```

### Reset completo
```bash
# Parar tudo e remover volumes
docker-compose down -v

# Subir novamente
docker-compose up -d
```

## 📚 Documentação Completa

- [Arquitetura](docs/architecture.md)
- [Schema do Banco](docs/database-schema.md)
- [API Docs](docs/api-docs.md)
- [Deploy em Produção](docs/deployment.md)

## 🎯 Próximos Passos

1. ✅ Implantar sistema para testes
2. ✅ Explorar API no Swagger
3. ✅ Criar primeira unidade/loja
4. ✅ Cadastrar setores (Cozinha, Salão, Estoque)
5. ✅ Criar cargos (Gerente, Cozinheiro, Atendente)
6. ✅ Cadastrar usuários
7. ✅ Criar checklists (Abertura, Fechamento)
8. ✅ Criar tarefas
9. ✅ Atribuir tarefas aos funcionários
10. 🔄 Implementar frontend/mobile conforme necessidade

## 📞 Suporte

Para dúvidas ou problemas, consulte:
- Documentação em `/workspace/docs/`
- Logs dos containers: `docker-compose logs`
- Swagger UI: http://localhost:8003/docs

---

**TaskManager v1.0.0** - Desenvolvido para redes de restaurantes escaláveis 🚀
