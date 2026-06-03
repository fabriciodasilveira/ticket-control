# Plano de Implantação em Produção

## Pré-requisitos

### Infraestrutura Mínima

| Recurso | Especificação |
|---------|--------------|
| CPU | 4 vCPUs |
| RAM | 8 GB |
| Storage | 50 GB SSD |
| Network | 1 Gbps |

### Serviços Externos

- PostgreSQL (RDS ou similar)
- Redis (ElastiCache ou similar)
- Cloudflare R2 para armazenamento
- SMTP para envio de emails

## Passo a Passo

### 1. Configurar Banco de Dados

```sql
-- Criar database
CREATE DATABASE taskmanager;
CREATE USER taskmanager_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE taskmanager TO taskmanager_user;
```

### 2. Configurar Variáveis de Ambiente

```bash
# .env.production
DATABASE_URL=postgresql://taskmanager_user:secure_password@db_host:5432/taskmanager
REDIS_URL=redis://redis_host:6379/0
SECRET_KEY=<gerar-chave-segura>
DEBUG=false
CORS_ORIGINS=["https://app.taskmanager.com"]

# Cloudflare R2
R2_ACCOUNT_ID=seu_account_id
R2_ACCESS_KEY_ID=sua_access_key
R2_SECRET_ACCESS_KEY=sua_secret_key
R2_BUCKET_NAME=taskmanager-evidence
R2_PUBLIC_URL=https://cdn.taskmanager.com
```

### 3. Build e Deploy

```bash
# Backend
cd backend
docker build -t taskmanager-backend:latest .
docker push registry/taskmanager-backend:latest

# Frontend
cd frontend
docker build -t taskmanager-frontend:latest .
docker push registry/taskmanager-frontend:latest
```

### 4. Deploy com Docker Compose (Produção)

```bash
cd infrastructure
docker-compose -f docker-compose.prod.yml up -d
```

### 5. Configurar Nginx (SSL)

```bash
# Gerar certificado SSL
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem

# Reiniciar nginx
docker-compose restart nginx
```

### 6. Executar Migrações

```bash
docker-compose exec backend alembic upgrade head
```

### 7. Criar Usuário Admin Inicial

```python
# script_create_admin.py
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()

admin = User(
    email="admin@taskmanager.com",
    password_hash=get_password_hash("Admin@123"),
    full_name="Administrador",
    role="admin"
)

db.add(admin)
db.commit()
db.close()
```

## Monitoramento

### Health Checks

```bash
# Verificar saúde da API
curl https://api.taskmanager.com/health

# Verificar banco de dados
docker-compose exec postgres pg_isready
```

### Logs

```bash
# Logs do backend
docker-compose logs -f backend

# Logs do nginx
docker-compose logs -f nginx
```

### Métricas

Configurar:
- Prometheus para métricas
- Grafana para dashboards
- AlertManager para alertas

## Backup

### Database

```bash
# Backup diário
0 2 * * * pg_dump -h db_host -U taskmanager_user taskmanager | gzip > /backups/db_$(date +\%Y\%m\%d).sql.gz
```

### Evidências (R2)

- Habilitar versioning no bucket
- Configurar lifecycle policies
- Replicação cross-region

## Escalabilidade

### Horizontal

```yaml
# docker-compose.prod.yml
services:
  backend:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 1G
```

### Load Balancer

Configurar AWS ALB ou similar:
- Health check: /health
- Sticky sessions: habilitado
- SSL termination: no LB

## Segurança

### Firewall

```
Portas abertas:
- 443 (HTTPS)
- 80 (HTTP -> redirect HTTPS)

Portas internas (VPC only):
- 5432 (PostgreSQL)
- 6379 (Redis)
- 8000 (Backend)
```

### Hardening

- Atualizar pacotes regularmente
- Usar secrets management (AWS Secrets Manager)
- Habilitar WAF
- Configurar rate limiting
- Implementar fail2ban

## CI/CD Pipeline

```yaml
# GitHub Actions
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pytest
    
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: docker build -t taskmanager-backend .
      - run: docker push registry/taskmanager-backend
      
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: ssh deploy@server "cd /app && docker-compose pull && docker-compose up -d"
```

## Rollback

```bash
# Em caso de problemas
docker-compose down
docker-compose up -d --force-recreate taskmanager-backend:previous-tag
```

## Checklist de Go-Live

- [ ] Database configurado e migrado
- [ ] Variáveis de ambiente definidas
- [ ] SSL configurado
- [ ] Backups automatizados
- [ ] Monitoramento ativo
- [ ] Logs centralizados
- [ ] Admin user criado
- [ ] Testes de carga realizados
- [ ] Documentação atualizada
- [ ] Equipe treinada

## Suporte

Em caso de problemas:

1. Verificar logs: `docker-compose logs`
2. Checar health: `curl /health`
3. Validar DB: `pg_isready`
4. Revisar métricas no Grafana
