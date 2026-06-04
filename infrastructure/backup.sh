#!/bin/bash

# Script de Backup e Restore - Task Manager
# Uso: 
#   ./backup.sh (para backup)
#   ./backup.sh restore <arquivo_backup.sql> (para restore)

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

BACKUP_DIR="./backups"
CONTAINER_NAME="taskmanager-db"
DB_NAME="taskmanager"
DB_USER="postgres"

# Criar diretório de backups
mkdir -p "$BACKUP_DIR"

# Função de backup
do_backup() {
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/backup_${TIMESTAMP}.sql"
    
    print_status "Iniciando backup do banco de dados..."
    
    # Verificar se container está rodando
    if ! docker ps | grep -q "$CONTAINER_NAME"; then
        print_error "Container $CONTAINER_NAME não está rodando!"
        exit 1
    fi
    
    # Executar backup
    docker exec "$CONTAINER_NAME" pg_dump -U "$DB_USER" "$DB_NAME" > "$BACKUP_FILE"
    
    # Comprimir backup
    gzip "$BACKUP_FILE"
    
    print_status "Backup criado com sucesso: ${BACKUP_FILE}.gz"
    
    # Listar backups existentes
    echo ""
    print_status "Backups existentes:"
    ls -lh "$BACKUP_DIR"/*.gz 2>/dev/null || echo "  Nenhum backup encontrado"
}

# Função de restore
do_restore() {
    BACKUP_FILE="$1"
    
    if [ -z "$BACKUP_FILE" ]; then
        print_error "Arquivo de backup não especificado!"
        echo "Uso: $0 restore <arquivo_backup.sql.gz>"
        exit 1
    fi
    
    if [ ! -f "$BACKUP_FILE" ]; then
        print_error "Arquivo de backup não encontrado: $BACKUP_FILE"
        exit 1
    fi
    
    print_warning "ATENÇÃO: Isso irá sobrescrever todos os dados do banco!"
    read -p "Tem certeza que deseja continuar? (yes/no): " confirm
    
    if [ "$confirm" != "yes" ]; then
        print_status "Operação cancelada"
        exit 0
    fi
    
    print_status "Iniciando restore do banco de dados..."
    
    # Verificar se container está rodando
    if ! docker ps | grep -q "$CONTAINER_NAME"; then
        print_error "Container $CONTAINER_NAME não está rodando!"
        exit 1
    fi
    
    # Descomprimir e restaurar
    if [[ "$BACKUP_FILE" == *.gz ]]; then
        gunzip -c "$BACKUP_FILE" | docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME"
    else
        cat "$BACKUP_FILE" | docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME"
    fi
    
    print_status "Restore concluído com sucesso!"
}

# Listar backups
list_backups() {
    print_status "Backups disponíveis:"
    echo ""
    ls -lh "$BACKUP_DIR"/*.gz 2>/dev/null || echo "  Nenhum backup encontrado"
    echo ""
    print_status "Para restaurar, use: $0 restore <arquivo_backup.sql.gz>"
}

# Main
case "$1" in
    restore)
        do_restore "$2"
        ;;
    list)
        list_backups
        ;;
    *)
        echo "=========================================="
        echo "  Task Manager - Backup/Restore"
        echo "=========================================="
        echo ""
        echo "Uso:"
        echo "  $0          - Criar backup"
        echo "  $0 restore <arquivo>  - Restaurar backup"
        echo "  $0 list     - Listar backups disponíveis"
        echo ""
        do_backup
        ;;
esac
