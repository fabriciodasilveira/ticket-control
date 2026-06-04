"""
Aplicação FastAPI principal
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time

from app.core.config import settings
from app.db.session import engine, Base
from app.api.v1.routes import auth, users, tasks, checklists, units, sectors, dashboard, reports

# Importar todos os modelos para registrar no SQLAlchemy
from app.models import Unit, Position, Sector, User, UserPosition, Task, Checklist, ChecklistTask
from app.models import TaskAssignment, Evidence, TemperatureRecord, Alert, Notification, AuditLog, SyncQueue, DashboardCache


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciador de ciclo de vida da aplicação"""
    # Startup
    print(f"Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Criar tabelas do banco (em produção usar migrations)
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Shutdown
    print("Fechando aplicação...")


# Criar aplicação FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Sistema de gerenciamento de tarefas, checklists e auditorias operacionais para hamburguerias e restaurantes",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware de logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Handler de exceções global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Erro interno do servidor",
            "detail": str(exc) if settings.DEBUG else "Ocorreu um erro inesperado"
        }
    )


# Rotas da API v1
app.include_router(auth.router, prefix=f"{settings.API_PREFIX}/auth", tags=["Autenticação"])
app.include_router(users.router, prefix=f"{settings.API_PREFIX}/users", tags=["Usuários"])
app.include_router(tasks.router, prefix=f"{settings.API_PREFIX}/tasks", tags=["Tarefas"])
app.include_router(checklists.router, prefix=f"{settings.API_PREFIX}/checklists", tags=["Checklists"])
app.include_router(units.router, prefix=f"{settings.API_PREFIX}/units", tags=["Unidades"])
app.include_router(sectors.router, prefix=f"{settings.API_PREFIX}/sectors", tags=["Setores"])
app.include_router(dashboard.router, prefix=f"{settings.API_PREFIX}/dashboard", tags=["Dashboard"])
app.include_router(reports.router, prefix=f"{settings.API_PREFIX}/reports", tags=["Relatórios"])


@app.get("/", tags=["Health"])
async def root():
    """Endpoint de health check"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Verifica saúde da aplicação"""
    return {
        "status": "healthy",
        "timestamp": time.time()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8003,
        reload=settings.DEBUG
    )
