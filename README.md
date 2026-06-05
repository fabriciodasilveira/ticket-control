# TaskManager Burger

Sistema completo para gerenciamento de tarefas, checklists e auditorias operacionais para hamburguerias e restaurantes.

## 🚀 Visão Geral

Plataforma SaaS multi-tenant que permite:

- **Gestores**: Acompanhar execução de tarefas, visualizar dashboards e aprovar atividades
- **Funcionários**: Executar tarefas, enviar evidências fotográficas e acompanhar histórico
- **Administradores**: Gerenciar usuários, unidades, cargos e configurações do sistema

## ✨ Funcionalidades Principais

### Gestão de Tarefas
- Tarefas diárias, semanais, mensais e personalizadas
- Prioridades e tempos estimados
- Atribuição por usuário ou cargo
- Status: Pendente, Em andamento, Concluída, Aprovada, Reprovada

### Checklists Operacionais
- Abertura e fechamento de loja
- Limpeza e higienização
- Segurança alimentar
- Controle de temperatura

### Evidências Fotográficas
- Upload de fotos com compressão automática
- Armazenamento no Cloudflare R2
- Organização por loja/usuário/data

### Dashboard Gerencial
- Indicadores de desempenho
- Taxa de conclusão e SLA
- Ranking de colaboradores
- Heatmap de execução

### Recursos Avançados
- QR Code por área/setor
- Modo offline (mobile)
- Assinatura digital
- Geolocalização
- Controle de temperatura com alertas
- Logs de auditoria completos

## 🏗️ Arquitetura

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Frontend Web  │     │   Mobile App    │     │   API Gateway   │
│   (Next.js)     │     │ (React Native)  │     │    (Nginx)      │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │      Backend API        │
                    │       (FastAPI)         │
                    └────────────┬────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌────────▼────────┐   ┌─────────▼────────┐   ┌─────────▼────────┐
│   PostgreSQL    │   │      Redis       │   │  Cloudflare R2   │
│   (Database)    │   │     (Cache)      │   │   (Storage)      │
└─────────────────┘   └──────────────────┘   └──────────────────┘
```

## 📁 Estrutura do Projeto

```
/workspace
├── backend/           # API FastAPI (Python)
├── frontend/          # Web App (Next.js + React)
├── mobile/            # App Mobile (React Native + Expo)
├── infrastructure/    # Docker, Nginx, Deploy
└── docs/             # Documentação técnica
```

## 🔧 Stack Tecnológico

### Backend
- Python 3.11+
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL 15
- Redis 7
- JWT Authentication

### Frontend Web
- Next.js 14
- React 18
- TypeScript
- TailwindCSS
- React Query

### Mobile
- React Native
- Expo
- TypeScript
- AsyncStorage (offline)

### Infraestrutura
- Docker & Docker Compose
- Nginx (reverse proxy)
- Cloudflare R2 (storage)

## 🚀 Quick Start

### Opção 1: Script Automático (Recomendado)

```bash
cd /workspace
./setup-test.sh
```

Este script irá automaticamente:
- Verificar dependências (Docker, Docker Compose)
- Iniciar PostgreSQL, Redis e Backend API
- Criar usuário administrador
- Mostrar informações de acesso

### Opção 2: Manual com Docker Compose

```bash
# 1. Acessar diretório de infraestrutura
cd /workspace/infrastructure

# 2. Copiar arquivo de ambiente
cp .env.example .env

# 3. Iniciar serviços (PostgreSQL, Redis, Backend)
docker-compose up -d postgres redis backend

# 4. Aguardar inicialização (~15 segundos)
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
print('✅ Admin criado!')
"

# 6. Acessar a API
# Swagger UI: http://localhost:8003/docs
```

### Opção 3: Implantação Completa (Frontend + Backend)

```bash
cd /workspace/infrastructure
docker-compose up -d
```

Isso iniciará todos os serviços incluindo o frontend web.

---

## 📍 Acessar o Sistema

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

## 👥 Perfis de Usuário

| Perfil | Permissões |
|--------|-----------|
| **Administrador** | CRUD completo, gestão de usuários, configurações |
| **Gerente** | Visualizar/approvar tarefas, gerenciar equipe da unidade |
| **Funcionário** | Executar tarefas atribuídas, enviar evidências |

## 📊 Modelos de Dados

Principais entidades:

- **Units**: Lojas/unidades
- **Users**: Usuários do sistema
- **Positions**: Cargos/funções
- **Sectors**: Setores da unidade
- **Tasks**: Tarefas
- **Checklists**: Listas de verificação
- **TaskAssignments**: Atribuições de tarefa
- **Evidence**: Fotos/evidências
- **TemperatureRecords**: Registros de temperatura
- **AuditLogs**: Logs de auditoria

## 🔐 Segurança

- Autenticação JWT com refresh token
- Hash de senhas com bcrypt
- RBAC (Role Based Access Control)
- CORS configurado
- Rate limiting
- SQL injection prevention
- XSS protection

## 📱 Recursos Mobile

### Modo Offline
- Execução de tarefas sem internet
- Armazenamento local (AsyncStorage)
- Sincronização automática ao reconectar

### Câmera
- Captura de fotos direto no app
- Compressão automática
- Upload em segundo plano

### QR Code
- Leitura de QR Codes por setor
- Acesso rápido a checklists

## 📈 Próximas Fases

### Fase 2 - IA
- Verificação automática de fotos
- Detecção de problemas de limpeza
- Alertas preditivos

### Fase 3 - Integrações
- WhatsApp Business API
- ERP de restaurantes
- Sistemas de PDV

## 📄 Licença

Proprietário - Todos os direitos reservados

## 🤝 Contribuição

Para contribuir com o projeto:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

---

**Desenvolvido com ❤️ para o setor de food service**
