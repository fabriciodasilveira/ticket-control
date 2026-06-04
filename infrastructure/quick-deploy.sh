#!/bin/bash

# Script de Deploy Rápido - Task Manager
# Uso: ./quick-deploy.sh

set -e

echo "=========================================="
echo "  Task Manager - Script de Deploy"
echo "=========================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para imprimir status
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Verificar se Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker não está instalado!"
        echo ""
        echo "Instale o Docker com:"
        echo "  curl -fsSL https://get.docker.com -o get-docker.sh"
        echo "  sudo sh get-docker.sh"
        exit 1
    fi
    print_status "Docker instalado: $(docker --version)"
}

# Verificar se Docker Compose está instalado
check_docker_compose() {
    if command -v docker-compose &> /dev/null; then
        print_status "Docker Compose instalado: $(docker-compose --version)"
    elif docker compose version &> /dev/null; then
        print_status "Docker Compose instalado (plugin): $(docker compose version)"
        export COMPOSE_COMMAND="docker compose"
        return
    else
        print_error "Docker Compose não está instalado!"
        echo ""
        echo "Instale com:"
        echo "  sudo curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m)\" -o /usr/local/bin/docker-compose"
        echo "  sudo chmod +x /usr/local/bin/docker-compose"
        exit 1
    fi
    export COMPOSE_COMMAND="docker-compose"
}

# Verificar diretório
check_directory() {
    if [ ! -f "docker-compose.yml" ]; then
        print_error "docker-compose.yml não encontrado!"
        print_warning "Execute este script a partir do diretório infrastructure/"
        exit 1
    fi
    print_status "Diretório correto verificado"
}

# Configurar .env
setup_env() {
    if [ ! -f ".env" ]; then
        print_warning ".env não encontrado. Criando a partir do .env.example..."
        cp .env.example .env
        print_status "Arquivo .env criado"
        
        # Gerar SECRET_KEY aleatória
        if command -v python3 &> /dev/null; then
            SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
            sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
            print_status "SECRET_KEY gerada automaticamente"
        else
            print_warning "Python3 não disponível. Gere uma SECRET_KEY manualmente no arquivo .env"
        fi
    else
        print_status "Arquivo .env já existe"
    fi
    
    echo ""
    print_warning "IMPORTANTE: Revise o arquivo .env e ajuste:"
    echo "  - SECRET_KEY (deve ser única e segura)"
    echo "  - DEBUG (defina como false em produção)"
    echo "  - CORS_ORIGINS (adicione seus domínios)"
    echo ""
}

# Criar diretórios necessários
setup_directories() {
    print_status "Criando diretórios necessários..."
    
    # Diretório SSL
    if [ ! -d "nginx/ssl" ]; then
        mkdir -p nginx/ssl
        print_status "Diretório nginx/ssl criado"
    fi
    
    # Diretório de dados do PostgreSQL (se usar volume bind)
    if [ ! -d "postgres_data" ] && grep -q "postgres_data:" docker-compose.yml; then
        # O volume será criado automaticamente pelo Docker
        print_status "Volume postgres_data será criado automaticamente"
    fi
}

# Iniciar serviços
start_services() {
    echo ""
    print_status "Iniciando serviços com Docker Compose..."
    echo ""
    
    # Parar serviços existentes
    $COMPOSE_COMMAND down 2>/dev/null || true
    
    # Construir e iniciar
    if [ "$1" == "production" ]; then
        print_status "Modo PRODUÇÃO (com Nginx e SSL)"
        $COMPOSE_COMMAND --profile production up -d --build
    else
        print_status "Modo DESENVOLVIMENTO (sem Nginx)"
        $COMPOSE_COMMAND up -d --build
    fi
    
    echo ""
    print_status "Aguardando serviços iniciarem..."
    sleep 10
}

# Verificar saúde dos serviços
check_health() {
    print_status "Verificando saúde dos serviços..."
    echo ""
    
    $COMPOSE_COMMAND ps
    
    echo ""
    
    # Verificar backend
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        print_status "Backend está saudável"
    else
        print_warning "Backend ainda não está respondendo (pode estar iniciando)"
    fi
    
    # Verificar frontend
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        print_status "Frontend está acessível"
    else
        print_warning "Frontend ainda não está respondendo (pode estar iniciando)"
    fi
}

# Mostrar logs
show_logs() {
    echo ""
    print_warning "Para ver os logs em tempo real, execute:"
    echo "  $COMPOSE_COMMAND logs -f"
    echo ""
    print_warning "Para acessar a aplicação:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend API: http://localhost:8000/api/v1"
    echo "  Swagger Docs: http://localhost:8000/docs"
    echo ""
}

# Main
main() {
    check_docker
    check_docker_compose
    check_directory
    setup_env
    setup_directories
    
    # Verificar modo de operação
    MODE="development"
    if [ "$1" == "--production" ] || [ "$1" == "-p" ]; then
        MODE="production"
    fi
    
    start_services $MODE
    check_health
    show_logs
    
    print_status "Deploy concluído!"
}

# Executar
main "$@"
