import logging
import time

from fastapi import APIRouter, HTTPException, status

from app.api.deps import PaginationDep, SessionDep
from app.metrics import (
    accidents_created_total,
    accidents_read_total,
    accidents_total,
    db_query_duration_seconds,
    http_errors_total,
)
from app.models.accident import Accident
from app.repositories.accident_repository import AccidentRepository
from app.schemas.accident import AccidentInput
from app.services.accident_service import AccidentService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/predict", response_model=Accident, status_code=status.HTTP_201_CREATED)
def predict_accident(data: AccidentInput, session: SessionDep):
    logger.info("📥 Nouvelle requête de prédiction")
    try:
        repository = AccidentRepository(session)
        service = AccidentService(repository)

        start = time.time()
        result = service.predict_and_save(data)
        db_query_duration_seconds.observe(time.time() - start)

        accidents_created_total.inc()  # ← APRÈS le succès
        accidents_total.inc()

        gravite = result.gravite_predite
        logger.info(f"✅ Prédiction - ID: {result.id}, Gravité: {gravite}")

        return result

    except Exception as e:
        logger.error(f"❌ Erreur: {e}", exc_info=True)
        http_errors_total.labels(error_type="server_error").inc()
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/", response_model=list[Accident])
def get_accidents(session: SessionDep, pagination: PaginationDep):
    start = time.time()
    repository = AccidentRepository(session)
    service = AccidentService(repository)
    result = service.get_all_accidents(**pagination)
    db_query_duration_seconds.observe(time.time() - start)
    accidents_read_total.inc()  # ← APRÈS le succès
    return result


@router.get("/{accident_id}", response_model=Accident)
def get_accident(accident_id: int, session: SessionDep):
    try:
        start = time.time()
        repository = AccidentRepository(session)
        service = AccidentService(repository)
        result = service.get_accident(accident_id)
        db_query_duration_seconds.observe(time.time() - start)
        accidents_read_total.inc()  # ← APRÈS le succès
        return result
    except ValueError as e:
        http_errors_total.labels(error_type="not_found").inc()
        raise HTTPException(status_code=404, detail=str(e)) from e
