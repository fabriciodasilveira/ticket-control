#!/bin/bash

# Script de inicialização rápida para testes
# TaskManager - Sistema de Gestão de Tarefas e Checklists

set -e

echo "=========================================="
echo "  TaskManager - Inicialização para Testes"
echo "=========================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para verificar dependências
check_dependencies() {
    echo "Verificando dependências..."
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker não está instalado${NC}"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}❌ Docker Compose não está instalado${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Docker e Docker Compose instalados${NC}"
    echo ""
}

# Função para iniciar serviços
start_services() {
    echo "Iniciando serviços com Docker Compose..."
    
    cd "$(dirname "$0")/infrastructure"
    
    # Copiar .env se não existir
    if [ ! -f .env ]; then
        echo "Criando arquivo .env a partir do exemplo..."
        cp .env.example .env
    fi
    
    # Iniciar PostgreSQL, Redis e Backend
    echo "Subindo containers (PostgreSQL, Redis, Backend)..."
    docker-compose up -d postgres redis backend
    
    echo ""
    echo -e "${YELLOW}⏳ Aguardando serviços iniciarem...${NC}"
    sleep 15
    
    # Verificar saúde dos serviços
    echo "Verificando saúde dos serviços..."
    
    if docker-compose ps postgres | grep -q "healthy"; then
        echo -e "${GREEN}✓ PostgreSQL saudável${NC}"
    else
        echo -e "${YELLOW}⚠ PostgreSQL ainda iniciando...${NC}"
    fi
    
    if docker-compose ps redis | grep -q "healthy"; then
        echo -e "${GREEN}✓ Redis saudável${NC}"
    else
        echo -e "${YELLOW}⚠ Redis ainda iniciando...${NC}"
    fi
    
    echo ""
}

# Função para criar usuário admin
create_admin_user() {
    echo "Criando usuário administrador..."
    
    cd "$(dirname "$0")/infrastructure"
    
    # Esperar backend estar pronto
    echo "Aguardando backend estar disponível..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Backend disponível${NC}"
            break
        fi
        if [ $i -eq 30 ]; then
            echo -e "${RED}❌ Backend não respondeu após 30 tentativas${NC}"
            exit 1
        fi
        sleep 2
    done
    
    # Criar admin via script Python
    echo "Executando script de criação de admin..."
    docker-compose exec -T backend python << 'PYTHON_SCRIPT'
import sys
sys.path.append('/app')

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()

# Verificar se admin já existe
existing_admin = db.query(User).filter(User.email == "admin@taskmanager.com").first()

if existing_admin:
    print("Usuário admin já existe!")
else:
    admin = User(
        email="admin@taskmanager.com",
        password_hash=get_password_hash("Admin@123"),
        full_name="Administrador Geral",
        role="admin"
    )
    
    db.add(admin)
    db.commit()
    print("Usuário admin criado com sucesso!")

db.close()
PYTHON_SCRIPT
    
    echo ""
}

# Função para mostrar informações de acesso
show_access_info() {
    echo ""
    echo "=========================================="
    echo -e "${GREEN}  ✅ Implantação concluída com sucesso!${NC}"
    echo "=========================================="
    echo ""
    echo "📍 Serviços disponíveis:"
    echo ""
    echo "   🔹 API Backend:    http://localhost:8000"
    echo "   🔹 Swagger UI:     http://localhost:8000/docs"
    echo "   🔹 ReDoc:          http://localhost:8000/redoc"
    echo "   🔹 Health Check:   http://localhost:8000/health"
    echo ""
    echo "🔐 Credenciais de Administrador:"
    echo ""
    echo "   📧 Email:    admin@taskmanager.com"
    echo "   🔑 Senha:    Admin@123"
    echo ""
    echo "=========================================="
    echo ""
    echo "📋 Próximos passos:"
    echo ""
    echo "   1. Acesse http://localhost:8000/docs para explorar a API"
    echo "   2. Faça login com as credenciais acima"
    echo "   3. Crie unidades, setores, cargos e usuários"
    echo "   4. Crie tarefas e checklists"
    echo "   5. Atribua tarefas aos funcionários"
    echo ""
    echo "=========================================="
    echo ""
    echo "Comandos úteis:"
    echo ""
    echo "   📊 Ver logs:           docker-compose logs -f"
    echo "   ⏹️  Parar serviços:     docker-compose down"
    echo "   🔄 Reiniciar backend:  docker-compose restart backend"
    echo "   💾 Reset completo:     docker-compose down -v"
    echo ""
    echo "=========================================="
    echo ""
}

# Executar todas as funções
check_dependencies
start_services
create_admin_user
show_access_info

echo -e "${GREEN}🎉 Tudo pronto! Boa sorte nos testes!${NC}"
echo ""
