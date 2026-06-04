# Mapeamento de Portas Alterado

Para evitar conflitos com serviços já em execução no seu servidor, as portas foram alteradas no `docker-compose.yml`:

## Portas Externas (Acesso do Host)

| Serviço | Porta Antiga | **Nova Porta** | Porta Interna (Container) |
|---------|-------------|----------------|---------------------------|
| PostgreSQL | 5432 | **5433** | 5432 |
| Redis | 6379 | **6380** | 6379 |
| Backend API | 8000 | **8001** | 8000 |
| Frontend | 3000 | **3001** | 3000 |
| Nginx HTTP | 80 | **8081** | 80 |
| Nginx HTTPS | 443 | **4433** | 443 |

## Como Acessar os Serviços

- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:8001/api/v1
- **PostgreSQL**: localhost:5433
- **Redis**: localhost:6380
- **Nginx (produção)**: http://localhost:8081

## Comandos para Deploy

```bash
# Parar e remover containers antigos (se houver)
cd infrastructure
docker-compose down -v

# Subir todos os serviços
docker-compose up -d --build

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f
```

## Se ainda houver conflito de portas

Caso alguma dessas novas portas também esteja em uso, execute:

```bash
# Ver quais portas estão em uso
sudo netstat -tulpn | grep LISTEN
# ou
sudo ss -tulpn | grep LISTEN

# Pare o serviço conflitante ou altere as portas no docker-compose.yml
```

## Produção

Para deploy em produção com Nginx:

```bash
docker-compose --profile production up -d --build
```

Certifique-se de configurar o SSL no diretório `infrastructure/nginx/ssl/` antes de usar o perfil de produção.
