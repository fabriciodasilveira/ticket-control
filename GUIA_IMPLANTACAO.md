# Guia de Implantação - Task Manager

Este guia descreve como fazer deploy da aplicação em um servidor usando Docker e PostgreSQL.

## Pré-requisitos

- Docker (versão 20.10 ou superior)
- Docker Compose (versão 2.0 ou superior)
- Git
- Acesso root ou usuário com permissões sudo

## Passo 1: Preparar o Servidor

### 1.1 Instalar Docker e Docker Compose (se necessário)

```bash
# Atualizar pacotes
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Adicionar usuário ao grupo docker (opcional, para não usar sudo)
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalações
docker --version
docker-compose --version
```

### 1.2 Configurar Firewall (opcional mas recomendado)

```bash
# Permitir apenas portas necessárias
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

## Passo 2: Clonar o Repositório

```bash
# Criar diretório para a aplicação
sudo mkdir -p /opt/taskmanager
cd /opt/taskmanager

# Clonar repositório (substitua pela URL do seu repositório)
git clone <URL_DO_REPOSITORIO> .
```

## Passo 3: Configurar Variáveis de Ambiente

```bash
# Navegar para diretório de infraestrutura
cd /opt/taskmanager/infrastructure

# Copiar arquivo de exemplo
cp .env.example .env

# Editar arquivo .env com suas configurações
nano .env
```

### Configurações Importantes no `.env`:

```bash
# Database (não altere se usar docker-compose padrão)
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/taskmanager

# Security - GERE UMA CHAVE SECRETA FORTE
SECRET_KEY=sua-chave-secreta-muito-forte-e-aleatoria-aqui

# Debug - Deixe false em produção
DEBUG=false

# CORS - Adicione seus domínios
CORS_ORIGINS=["https://seu-dominio.com", "https://www.seu-dominio.com"]

# Cloudflare R2 (Opcional - para upload de evidências)
R2_ACCOUNT_ID=sua-account-id
R2_ACCESS_KEY_ID=sua-access-key
R2_SECRET_ACCESS_KEY=sua-secret-key
R2_BUCKET_NAME=taskmanager-evidence
R2_PUBLIC_URL=https://cdn.seu-dominio.com

# Email SMTP (Opcional - para notificações)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=sua-senha-de-app
SMTP_FROM_EMAIL=noreply@seu-dominio.com
```

### Gerar SECRET_KEY Forte:

```bash
# Gerar chave aleatória segura
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Passo 4: Configurar SSL/TLS (Recomendado para Produção)

### 4.1 Obter Certificado SSL (Let's Encrypt)

```bash
# Instalar Certbot
sudo apt install certbot -y

# Parar nginx temporariamente se estiver rodando
sudo systemctl stop nginx || true

# Obter certificado
sudo certbot certonly --standalone -d seu-dominio.com -d www.seu-dominio.com

# Os certificados estarão em:
# /etc/letsencrypt/live/seu-dominio.com/
```

### 4.2 Configurar Nginx com SSL

```bash
# Criar diretório para certificados no projeto
mkdir -p /opt/taskmanager/infrastructure/nginx/ssl

# Copiar certificados
sudo cp /etc/letsencrypt/live/seu-dominio.com/fullchain.pem /opt/taskmanager/infrastructure/nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/seu-dominio.com/privkey.pem /opt/taskmanager/infrastructure/nginx/ssl/key.pem

# Configurar permissões
sudo chmod 644 /opt/taskmanager/infrastructure/nginx/ssl/cert.pem
sudo chmod 600 /opt/taskmanager/infrastructure/nginx/ssl/key.pem
```

### 4.3 Atualizar Configuração do Nginx

Edite `/opt/taskmanager/infrastructure/nginx/nginx.conf` e atualize as configurações de SSL:

```nginx
server {
    listen 443 ssl http2;
    server_name seu-dominio.com www.seu-dominio.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # ... resto da configuração
}
```

## Passo 5: Iniciar a Aplicação

### 5.1 Modo Desenvolvimento (sem Nginx/SSL)

```bash
cd /opt/taskmanager/infrastructure

# Iniciar todos os serviços exceto nginx
docker-compose up -d

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f
```

### 5.2 Modo Produção (com Nginx e SSL)

```bash
cd /opt/taskmanager/infrastructure

# Iniciar todos os serviços incluindo nginx
docker-compose --profile production up -d

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f
```

## Passo 6: Acessar a Aplicação

- **Frontend**: http://localhost:3001 (ou https://seu-dominio.com em produção)
- **Backend API**: http://localhost:8003/api/v1 (ou https://seu-dominio.com/api/v1 em produção)
- **Documentação Swagger**: http://localhost:8003/docs

## Passo 7: Criar Usuário Administrador

Após iniciar a aplicação, crie o primeiro usuário admin:

```bash
# Acessar container do backend
docker exec -it taskmanager-backend bash

# Rodar script de criação de admin (se disponível)
python scripts/create_admin.py

# OU usar a API diretamente
curl -X POST http://localhost:8003/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@seu-dominio.com",
    "password": "SenhaForte123!",
    "full_name": "Administrador",
    "role": "admin"
  }'
```

## Comandos Úteis

### Ver Logs

```bash
# Todos os serviços
docker-compose logs -f

# Serviço específico
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Reiniciar Serviços

```bash
# Reiniciar tudo
docker-compose restart

# Reiniciar serviço específico
docker-compose restart backend
```

### Parar Aplicação

```bash
# Parar todos os serviços
docker-compose down

# Parar e remover volumes (CUIDADO: apaga dados!)
docker-compose down -v
```

### Atualizar Aplicação

```bash
cd /opt/taskmanager

# Puxar novas alterações
git pull

# Reconstruir containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Ou com profile production
docker-compose --profile production down
docker-compose --profile production build --no-cache
docker-compose --profile production up -d
```

### Backup do Banco de Dados

```bash
# Criar backup
docker exec taskmanager-db pg_dump -U postgres taskmanager > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar backup
cat backup_YYYYMMDD_HHMMSS.sql | docker exec -i taskmanager-db psql -U postgres taskmanager
```

### Monitoramento

```bash
# Uso de recursos
docker stats

# Espaço em disco
docker system df

# Limpar recursos não utilizados
docker system prune -a
```

## Troubleshooting

### Container não inicia

```bash
# Ver logs detalhados
docker-compose logs backend

# Verificar se portas estão em uso
sudo netstat -tulpn | grep :8003
sudo netstat -tulpn | grep :3001
sudo netstat -tulpn | grep :5434
```

### Erro de conexão com banco de dados

```bash
# Verificar se postgres está saudável
docker-compose ps postgres

# Testar conexão
docker exec -it taskmanager-db psql -U postgres -d taskmanager -c "SELECT 1;"
```

### Permissões de volume

```bash
# Corrigir permissões
sudo chown -R 999:999 /opt/taskmanager/infrastructure/postgres_data
```

### Resetar aplicação completamente

```bash
# PARAR TUDO E REMOVER DADOS (CUIDADO!)
cd /opt/taskmanager/infrastructure
docker-compose down -v

# Remover volumes manualmente se necessário
sudo rm -rf postgres_data
sudo rm -rf redis_data

# Recriar
docker-compose up -d
```

## Segurança em Produção

1. **Alterar todas as senhas padrão**
2. **Usar HTTPS obrigatoriamente**
3. **Configurar firewall adequadamente**
4. **Manter Docker e sistema atualizados**
5. **Usar variáveis de ambiente seguras**
6. **Implementar backup automático**
7. **Configurar monitoramento e alertas**
8. **Restringir acesso ao banco de dados**
9. **Usar redes Docker isoladas**
10. **Implementar rate limiting**

## Suporte

Para mais informações, consulte:
- README.md na raiz do projeto
- Documentação da API: /docs
- Logs dos containers
