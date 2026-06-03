# Documentação da API

## Base URL

```
Development: http://localhost:8000/api/v1
Production: https://api.taskmanager.com/api/v1
```

## Autenticação

A API utiliza JWT (JSON Web Tokens) para autenticação.

### Obter Token

```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=email@exemplo.com&password=sua-senha
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Usar Token

Incluir no header das requisições:

```
Authorization: Bearer <access_token>
```

## Endpoints

### Autenticação

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/auth/register` | Registrar novo usuário |
| POST | `/auth/login` | Login |
| POST | `/auth/logout` | Logout |
| POST | `/auth/refresh` | Renovar token |
| GET | `/auth/me` | Perfil atual |

### Usuários

| Método | Endpoint | Descrição | Permissão |
|--------|----------|-----------|-----------|
| GET | `/users` | Listar usuários | Todos |
| POST | `/users` | Criar usuário | Admin |
| GET | `/users/{id}` | Obter usuário | Todos |
| PUT | `/users/{id}` | Atualizar usuário | Self/Admin |
| DELETE | `/users/{id}` | Excluir usuário | Admin |
| POST | `/users/{id}/deactivate` | Desativar usuário | Manager+ |

### Tarefas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/tasks` | Listar tarefas |
| POST | `/tasks` | Criar tarefa |
| GET | `/tasks/{id}` | Obter tarefa |
| PUT | `/tasks/{id}` | Atualizar tarefa |
| DELETE | `/tasks/{id}` | Excluir tarefa |
| POST | `/tasks/{id}/start` | Iniciar tarefa |
| POST | `/tasks/{id}/complete` | Completar tarefa |
| POST | `/tasks/{id}/approve` | Aprovar tarefa |
| POST | `/tasks/{id}/reject` | Reprovar tarefa |

### Checklists

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/checklists` | Listar checklists |
| POST | `/checklists` | Criar checklist |
| GET | `/checklists/{id}` | Obter checklist |
| PUT | `/checklists/{id}` | Atualizar checklist |
| DELETE | `/checklists/{id}` | Excluir checklist |
| POST | `/checklists/{id}/execute` | Executar checklist |

### Unidades

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/units` | Listar unidades |
| POST | `/units` | Criar unidade |
| GET | `/units/{id}` | Obter unidade |
| PUT | `/units/{id}` | Atualizar unidade |
| DELETE | `/units/{id}` | Excluir unidade |

### Setores

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/sectors` | Listar setores |
| POST | `/sectors` | Criar setor |
| GET | `/sectors/{id}` | Obter setor |
| PUT | `/sectors/{id}` | Atualizar setor |
| DELETE | `/sectors/{id}` | Excluir setor |

### Dashboard

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/dashboard/metrics` | Métricas gerais |
| GET | `/dashboard/charts/completion-rate` | Taxa de conclusão |
| GET | `/dashboard/charts/tasks-by-status` | Tarefas por status |
| GET | `/dashboard/ranking/employees` | Ranking funcionários |
| GET | `/dashboard/heatmap` | Heatmap execução |

### Relatórios

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/reports/tasks` | Relatório de tarefas |
| GET | `/reports/employees` | Relatório funcionários |
| GET | `/reports/export/pdf` | Exportar PDF |
| GET | `/reports/export/excel` | Exportar Excel |
| GET | `/reports/export/csv` | Exportar CSV |

### Evidências

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/evidence/upload` | Upload de foto |
| GET | `/evidence/{id}` | Obter evidência |
| DELETE | `/evidence/{id}` | Excluir evidência |
| GET | `/evidence/task/{task_id}` | Evidências da tarefa |

### Temperatura

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/temperature` | Registrar temperatura |
| GET | `/temperature/history` | Histórico |
| GET | `/temperature/alerts` | Alertas ativos |

## Códigos de Status

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 201 | Criado |
| 204 | Sem conteúdo |
| 400 | Requisição inválida |
| 401 | Não autorizado |
| 403 | Proibido |
| 404 | Não encontrado |
| 409 | Conflito |
| 422 | Erro de validação |
| 500 | Erro interno |

## Rate Limiting

- 60 requisições por minuto por IP
- Header `X-RateLimit-Limit`: limite total
- Header `X-RateLimit-Remaining`: restantes
- Header `Retry-After`: segundos para retry

## Paginação

Endpoints de lista suportam:

```
GET /api/v1/users?page=1&page_size=20
```

Parâmetros:
- `page`: Número da página (default: 1)
- `page_size`: Itens por página (default: 20, max: 100)

Resposta inclui:
```json
{
  "items": [...],
  "total": 150,
  "page": 1,
  "page_size": 20,
  "pages": 8
}
```

## Filtros

Muitos endpoints suportam filtros via query params:

```
GET /api/v1/tasks?status=pending&priority=high&unit_id=uuid
```

## Exemplos de Uso

### Criar Tarefa

```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Limpar cozinha",
    "description": "Limpeza geral da cozinha",
    "sector_id": "uuid-do-setor",
    "priority": "high",
    "frequency": "daily",
    "photo_requirement": "required"
  }'
```

### Upload de Foto

```bash
curl -X POST http://localhost:8000/api/v1/evidence/upload \
  -H "Authorization: Bearer <token>" \
  -F "file=@foto.jpg" \
  -F "task_assignment_id=uuid-da-atribuicao" \
  -F "caption=Cozinha limpa"
```

### Completar Tarefa

```bash
curl -X POST http://localhost:8000/api/v1/tasks/{id}/complete \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "observations": "Tarefa concluída",
    "geolocation": {"lat": -23.5505, "lng": -46.6333},
    "execution_time": 15
  }'
```
