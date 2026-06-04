# TaskManager Burger - Backend

Backend API para sistema de gerenciamento de tarefas, checklists e auditorias operacionais.

## Requisitos

- Python 3.11+
- PostgreSQL 15+
- Redis 7+

## Instalação

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Copiar arquivo de ambiente
cp .env.example .env

# Executar migrações
alembic upgrade head

# Rodar servidor
uvicorn app.main:app --reload
```

## Variáveis de Ambiente

Copie `.env.example` para `.env` e configure:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/taskmanager

# Security
SECRET_KEY=sua-chave-secreta-aqui

# Cloudflare R2
R2_ACCOUNT_ID=
R2_ACCESS_KEY_ID=
R2_SECRET_ACCESS_KEY=
R2_BUCKET_NAME=taskmanager-evidence

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_USER=
SMTP_PASSWORD=
```

## API Documentation

Após rodar o servidor, acesse:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## Estrutura do Projeto

```
backend/
├── app/
│   ├── api/v1/routes/     # Rotas da API
│   ├── core/              # Configurações, segurança, exceções
│   ├── db/                # Conexão com banco de dados
│   ├── models/            # Modelos SQLAlchemy
│   ├── schemas/           # Schemas Pydantic
│   ├── services/          # Serviços de negócio
│   ├── utils/             # Utilitários
│   └── main.py            # Aplicação principal
├── tests/                 # Testes
├── requirements.txt       # Dependências
└── Dockerfile            # Docker
```

## Endpoints Principais

### Autenticação
- `POST /api/v1/auth/register` - Registrar usuário
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/logout` - Logout
- `GET /api/v1/auth/me` - Perfil atual

### Usuários
- `GET /api/v1/users` - Listar usuários
- `POST /api/v1/users` - Criar usuário
- `GET /api/v1/users/{id}` - Obter usuário
- `PUT /api/v1/users/{id}` - Atualizar usuário
- `DELETE /api/v1/users/{id}` - Excluir usuário

### Tarefas
- `GET /api/v1/tasks` - Listar tarefas
- `POST /api/v1/tasks` - Criar tarefa
- `GET /api/v1/tasks/{id}` - Obter tarefa
- `PUT /api/v1/tasks/{id}` - Atualizar tarefa

### Checklists
- `GET /api/v1/checklists` - Listar checklists
- `POST /api/v1/checklists` - Criar checklist

### Dashboard
- `GET /api/v1/dashboard/metrics` - Métricas
- `GET /api/v1/dashboard/charts/*` - Gráficos

### Relatórios
- `GET /api/v1/reports/tasks` - Relatório de tarefas
- `GET /api/v1/reports/export/pdf` - Exportar PDF

## Desenvolvimento

```bash
# Rodar testes
pytest

# Formatar código
black app/
isort app/

# Verificar tipos
mypy app/
```

## Docker

```bash
# Build
docker build -t taskmanager-backend .

# Run
docker run -p 8000:8000 --env-file .env taskmanager-backend
```
