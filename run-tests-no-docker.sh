#!/bin/bash

# Script de teste rápido sem Docker
# TaskManager - Sistema de Gestão de Tarefas e Checklists

set -e

echo "=========================================="
echo "  TaskManager - Teste Rápido (Sem Docker)"
echo "=========================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

cd "$(dirname "$0")/backend"

# Instalar dependências se necessário
echo "Verificando dependências Python..."
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo -e "${YELLOW}Instalando dependências...${NC}"
    pip3 install -r requirements.txt -q
fi

echo -e "${GREEN}✓ Dependências Python OK${NC}"
echo ""

# Criar arquivo .env para teste local
echo "Configurando ambiente de teste..."
cat > .env << 'EOF'
DATABASE_URL=sqlite:///./test_taskmanager.db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=test-secret-key-for-local-testing-123456
DEBUG=true
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
EOF

echo -e "${GREEN}✓ Ambiente configurado${NC}"
echo ""

# Iniciar backend em background
echo "Iniciando backend na porta 8000..."
cd /workspace/backend

# Matar processo anterior se existir
pkill -f "uvicorn app.main:app" 2>/dev/null || true
sleep 2

# Iniciar servidor
nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/backend.log 2>&1 &
BACKEND_PID=$!

echo "Backend iniciado com PID: $BACKEND_PID"
echo ""

# Aguardar backend estar pronto
echo -e "${YELLOW}⏳ Aguardando backend iniciar...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend disponível${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}❌ Backend não respondeu após 30 tentativas${NC}"
        echo "Logs do backend:"
        cat /tmp/backend.log
        exit 1
    fi
    sleep 2
done

echo ""

# Criar usuário admin via script Python
echo "Criando usuário administrador..."
python3 << 'PYTHON_SCRIPT'
import sys
sys.path.insert(0, '/workspace/backend')

from app.db.session import SessionLocal, engine, Base
from app.models.user import User
from app.core.security import get_password_hash

# Criar tabelas
Base.metadata.create_all(bind=engine)

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

# Mostrar informações de acesso
echo ""
echo "=========================================="
echo -e "${GREEN}  ✅ Backend pronto para testes!${NC}"
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
echo "   3. Use curl ou Postman para testar endpoints"
echo ""
echo "=========================================="
echo ""
echo "Comandos úteis:"
echo ""
echo "   📊 Ver logs:           tail -f /tmp/backend.log"
echo "   ⏹️  Parar backend:      pkill -f 'uvicorn app.main:app'"
echo "   🔄 Reiniciar:          pkill -f 'uvicorn app.main:app' && ./run-tests-no-docker.sh"
echo ""
echo "=========================================="
echo ""
echo -e "${GREEN}🎉 Tudo pronto! Boa sorte nos testes!${NC}"
echo ""

# Manter script rodando para mostrar logs
echo "Pressione Ctrl+C para parar o servidor..."
wait $BACKEND_PID
