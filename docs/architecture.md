# Arquitetura do Sistema - TaskManager Burger

## Visão Geral

Sistema completo para gerenciamento de tarefas, checklists e auditorias operacionais para hamburguerias e restaurantes.

## Stack Tecnológico

### Backend
- **Python 3.11+**
- **FastAPI** - Framework web assíncrono
- **SQLAlchemy 2.0** - ORM
- **PostgreSQL** - Banco de dados
- **Redis** - Cache e filas
- **Cloudflare R2** - Armazenamento de imagens
- **JWT** - Autenticação

### Frontend Web
- **React 18+**
- **Next.js 14** - Framework React
- **TailwindCSS** - Estilização
- **TypeScript** - Tipagem
- **React Query** - Gerenciamento de estado
- **Zustand** - Estado global

### Mobile
- **React Native**
- **Expo** - Desenvolvimento
- **TypeScript**
- **React Navigation** - Navegação
- **AsyncStorage** - Persistência offline
- **Expo Camera** - Captura de fotos

### Infraestrutura
- **Docker & Docker Compose**
- **Nginx** - Reverse proxy
- **GitHub Actions** - CI/CD

## Estrutura de Diretórios

```
/workspace
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── routes/
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── users.py
│   │   │   │   │   ├── tasks.py
│   │   │   │   │   ├── checklists.py
│   │   │   │   │   ├── units.py
│   │   │   │   │   ├── sectors.py
│   │   │   │   │   ├── positions.py
│   │   │   │   │   ├── reports.py
│   │   │   │   │   └── dashboard.py
│   │   │   │   └── deps.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── exceptions.py
│   │   ├── db/
│   │   │   ├── session.py
│   │   │   ├── base.py
│   │   │   └── init_db.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   ├── checklist.py
│   │   │   ├── unit.py
│   │   │   ├── sector.py
│   │   │   ├── position.py
│   │   │   ├── evidence.py
│   │   │   ├── audit_log.py
│   │   │   └── notification.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   ├── checklist.py
│   │   │   ├── unit.py
│   │   │   ├── sector.py
│   │   │   ├── position.py
│   │   │   ├── evidence.py
│   │   │   └── common.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── task_service.py
│   │   │   ├── checklist_service.py
│   │   │   ├── storage_service.py
│   │   │   ├── notification_service.py
│   │   │   ├── report_service.py
│   │   │   └── ai_service.py
│   │   ├── utils/
│   │   │   ├── image_processor.py
│   │   │   ├── qr_code.py
│   │   │   └── helpers.py
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── alembic/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── (dashboard)/
│   │   │   ├── (auth)/
│   │   │   └── api/
│   │   ├── components/
│   │   │   ├── ui/
│   │   │   ├── tasks/
│   │   │   ├── checklists/
│   │   │   ├── dashboard/
│   │   │   └── layout/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── stores/
│   │   ├── types/
│   │   └── utils/
│   ├── public/
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── Dockerfile
├── mobile/
│   ├── app/
│   │   ├── (tabs)/
│   │   ├── (auth)/
│   │   ├── tasks/
│   │   ├── checklists/
│   │   └── profile/
│   ├── components/
│   ├── hooks/
│   ├── services/
│   ├── store/
│   ├── types/
│   ├── utils/
│   ├── assets/
│   ├── app.json
│   ├── package.json
│   └── tsconfig.json
├── infrastructure/
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   ├── nginx/
│   │   └── nginx.conf
│   └── scripts/
├── docs/
│   ├── architecture.md
│   ├── database-schema.md
│   ├── api-docs.md
│   ├── deployment.md
│   └── wireframes/
└── README.md
```

## Diagrama de Entidades

### Usuários e Permissões
```
User (1) ----< (N) UserPosition
Position (1) ----< (N) UserPosition
User (1) ----< (N) Task
User (1) ----< (N) Evidence
User (1) ----< (N) AuditLog
```

### Unidades e Setores
```
Unit (1) ----< (N) Sector
Unit (1) ----< (N) User
Unit (1) ----< (N) Task
Sector (1) ----< (N) Task
Sector (1) ----< (N) Checklist
```

### Tarefas e Checklists
```
Checklist (1) ----< (N) ChecklistTask
Task (1) ----< (N) ChecklistTask
Task (1) ----< (N) Evidence
Task (1) ----< (N) TaskAssignment
Task (1) ----< (N) AuditLog
```

### Evidências
```
Evidence (N) ----> (1) Task
Evidence (N) ----> (1) User
Evidence (N) ----> (1) Unit
```

## Fluxo de Autenticação

1. Usuário faz login com email/senha
2. Backend valida credenciais
3. Gera JWT Access Token + Refresh Token
4. Frontend armazena tokens
5. Access Token enviado em cada requisição
6. Refresh Token usado para renovar acesso

## Fluxo de Execução de Tarefa

1. Funcionário visualiza tarefas atribuídas
2. Inicia tarefa (status: Em andamento)
3. Executa tarefa conforme descrição
4. Tira foto(s) obrigatória(s)
5. Adiciona observações
6. Marca como concluída
7. Gerente recebe notificação
8. Gerente aprova ou reprova
9. Se reprovada, retorna ao funcionário

## Modo Offline (Mobile)

1. Detecta perda de conexão
2. Salva ações localmente (AsyncStorage)
3. Exibe indicador de modo offline
4. Quando conectado, sincroniza fila
5. Confirma sincronização

## QR Code por Área

1. Gera QR Code único por setor/área
2. Funcionário escaneia com app
3. Abre checklist específico daquele local
4. Registra data/hora do scan

## Segurança

- Senhas hash com bcrypt
- JWT com expiração curta
- Refresh token rotativo
- CORS configurado
- Rate limiting
- Validação de input
- SQL injection prevention
- XSS protection

## Escalabilidade

- Database connection pooling
- Redis cache para consultas frequentes
- CDN para imagens (Cloudflare)
- Load balancer ready
- Horizontal scaling support
- Async operations com Celery
