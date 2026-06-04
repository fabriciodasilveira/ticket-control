# Guia Completo de Deploy - Task Manager

## 📋 Pré-requisitos

- Docker e Docker Compose instalados
- Git (para clonar o repositório)
- Acesso SSH ao servidor (para deploy remoto)

## 🚀 Problema de Portas Conflitantes

Se você encontrou erros como:
```
ERROR: Bind for 0.0.0.0:5432 failed: port is already allocated
```

Isso significa que algum serviço já está usando as portas padrão no seu servidor. Para resolver, **alteramos todas as portas externas** no `docker-compose.yml`.

## 📊 Novas Portas

| Serviço | Porta Externa (Host) | Porta Interna (Container) | URL de Acesso |
|---------|---------------------|---------------------------|---------------|
| PostgreSQL | 5433 | 5432 | localhost:5433 |
| Redis | 6380 | 6379 | localhost:6380 |
| Backend API | 8001 | 8000 | http://localhost:8001 |
| Frontend | 3001 | 3000 | http://localhost:3001 |
| Nginx HTTP | 8081 | 80 | http://localhost:8081 |
| Nginx HTTPS | 4433 | 443 | https://localhost:4433 |

> **Nota**: As portas internas dos containers NÃO foram alteradas. Apenas o mapeamento externo mudou.

## 📥 Download e Setup no Servidor

### Opção 1: Via Git (Recomendado)

```bash
# No seu servidor
cd /opt  # ou outro diretório de sua preferência
git clone <URL_DO_SEU_REPOSITORIO> taskmanager
cd taskmanager/infrastructure

# Copie o arquivo de ambiente
cp .env.example .env

# Edite o .env se necessário (mude SECRET_KEY em produção!)
nano .env
```

### Opção 2: Upload Manual

1. Baixe todos os arquivos do projeto
2. Faça upload para o servidor via SCP/SFTP:
```bash
# No seu computador local
scp -r ./project user@seu-servidor:/opt/taskmanager
```

3. No servidor:
```bash
cd /opt/taskmanager/infrastructure
cp .env.example .env
```

## 🔧 Configuração do Ambiente (.env)

Edite o arquivo `.env` com suas configurações:

```bash
# Database (NÃO ALTERE - as portas internas são fixas)
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/taskmanager

# Redis (NÃO ALTERE)
REDIS_URL=redis://redis:6379/0

# Security (ALTERE EM PRODUÇÃO!)
SECRET_KEY=sua-chave-secreta-muito-forte-e-aleatoria
DEBUG=false

# CORS (ALTERE conforme seu domínio)
CORS_ORIGINS=["https://seu-dominio.com"]
```

## 🎯 Deploy Passo a Passo

### 1. Parar Containers Antigos (se houver)

```bash
cd /opt/taskmanager/infrastructure
docker-compose down -v
```

### 2. Subir Todos os Serviços

```bash
docker-compose up -d --build
```

### 3. Verificar Status

```bash
# Ver containers rodando
docker-compose ps

# Ver logs em tempo real
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs backend
docker-compose logs postgres
```

### 4. Testar Acesso

```bash
# Testar Backend
curl http://localhost:8001/api/v1/health

# Testar Frontend (no navegador)
# Acesse: http://SEU_IP_SERVIDOR:3001
```

## 🌐 Deploy em Produção com Nginx

Para usar o Nginx como reverse proxy (produção):

```bash
# Configurar SSL primeiro (veja seção abaixo)
# Depois suba com o perfil de produção
docker-compose --profile production up -d --build
```

### Configurar SSL

1. Gere ou obtenha certificados SSL
2. Coloque os arquivos em `infrastructure/nginx/ssl/`:
   - `cert.pem` (ou `fullchain.pem`)
   - `key.pem` (ou `privkey.pem`)

3. Ou use Let's Encrypt:
```bash
# Instale certbot no host
sudo apt-get install certbot

# Gere certificados
sudo certbot certonly --standalone -d seu-dominio.com

# Copie para o diretório do nginx
sudo cp /etc/letsencrypt/live/seu-dominio.com/fullchain.pem infrastructure/nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/seu-dominio.com/privkey.pem infrastructure/nginx/ssl/key.pem
```

## 🔍 Troubleshooting

### Portas ainda em conflito?

Verifique quais portas estão em uso:

```bash
# Listar portas em uso
sudo netstat -tulpn | grep LISTEN
# ou
sudo ss -tulpn | grep LISTEN

# Matar processo usando a porta (cuidado!)
sudo kill -9 <PID>

# OU edite docker-compose.yml e use outras portas
```

### Containers não iniciam?

```bash
# Ver logs detalhados
docker-compose logs postgres
docker-compose logs backend

# Recriar containers
docker-compose down
docker-compose up -d --build --force-recreate

# Verificar espaço em disco
df -h
docker system df
```

### Banco de dados não persiste?

Os dados são salvos em volumes Docker. Para backup:

```bash
# Backup
docker-compose exec postgres pg_dump -U postgres taskmanager > backup.sql

# Restore
cat backup.sql | docker-compose exec -T postgres psql -U postgres taskmanager
```

### Reset completo (perde dados!)

```bash
docker-compose down -v --remove-orphans
docker-compose up -d --build
```

## 📊 Comandos Úteis

```bash
# Ver status de todos os serviços
docker-compose ps

# Reiniciar um serviço
docker-compose restart backend

# Parar tudo
docker-compose down

# Parar e remover volumes (cuidado: perde dados!)
docker-compose down -v

# Ver logs
docker-compose logs -f
docker-compose logs backend

# Acessar terminal do container
docker-compose exec backend bash
docker-compose exec postgres psql -U postgres

# Executar migrações (se houver)
docker-compose exec backend alembic upgrade head

# Ver uso de recursos
docker stats
```

## 🔐 Segurança em Produção

1. **Altere o SECRET_KEY** no `.env`
2. **Desative DEBUG**: `DEBUG=false`
3. **Configure CORS** apenas para seu domínio
4. **Use HTTPS** com certificado SSL válido
5. **Altere a senha do PostgreSQL** no `.env`
6. **Restrinja acesso** às portas no firewall do servidor

### Exemplo de Firewall (UFW)

```bash
# Habilitar UFW
sudo ufw enable

# Permitir apenas portas necessárias
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 8081/tcp  # Nginx HTTP
sudo ufw allow 4433/tcp  # Nginx HTTPS

# Bloquear acesso direto às outras portas
sudo ufw deny 5433/tcp
sudo ufw deny 6380/tcp
sudo ufw deny 8001/tcp
sudo ufw deny 3001/tcp
```

## 📈 Monitoramento

```bash
# Ver logs em tempo real
docker-compose logs -f

# Ver uso de CPU/Memória
docker stats

# Verificar saúde dos serviços
docker-compose ps
docker inspect taskmanager-db | grep -i health
```

## ✅ Checklist de Deploy

- [ ] Docker e Docker Compose instalados
- [ ] Arquivos copiados para o servidor
- [ ] `.env` configurado com SECRET_KEY forte
- [ ] DEBUG=false em produção
- [ ] SSL configurado (se usando HTTPS)
- [ ] Firewall configurado
- [ ] Backup agendado (use `backup.sh`)
- [ ] Testes de acesso realizados
- [ ] Monitoramento configurado

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs: `docker-compose logs -f`
2. Consulte a documentação em `/docs`
3. Verifique se as portas estão livres antes de subir
4. Certifique-se de ter espaço em disco suficiente

---

**URLs de Acesso após deploy:**
- Frontend: http://SEU_IP:3001
- API: http://SEU_IP:8001/api/v1
- Docs API: http://SEU_IP:8001/docs
