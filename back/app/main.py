from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging import logger, setup_logging
from app.database import create_db_and_tables

# Configurer le logging
setup_logging()

app = FastAPI(title=settings.PROJECT_NAME)

# Event handlers
@app.on_event("startup")
def on_startup():
    logger.info(f"🚀 Démarrage de {settings.PROJECT_NAME}")
    logger.info(f"📍 Environnement: {settings.ENV}")
    create_db_and_tables()
    logger.info("✅ Base de données initialisée")

@app.on_event("shutdown")
def on_shutdown():
    logger.info("🛑 Arrêt de l'application")

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"❌ Erreur de validation: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

# Routes
@app.get("/")
def root():
    return {"status": "API Accident Severity opérationnelle"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": settings.ENV}

# Inclure les routes API v1
app.include_router(api_router, prefix=settings.API_V1_STR)