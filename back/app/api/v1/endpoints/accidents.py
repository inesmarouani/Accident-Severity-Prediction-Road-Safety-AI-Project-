import logging
from typing import List

from fastapi import APIRouter, HTTPException, status

from app.api.deps import PaginationDep, SessionDep
from app.models.accident import Accident
from app.repositories.accident_repository import AccidentRepository
from app.schemas.accident import AccidentInput
from app.services.accident_service import AccidentService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/predict", response_model=Accident, status_code=status.HTTP_201_CREATED)
def predict_accident(data: AccidentInput, session: SessionDep):
    """Prédit la gravité d'un accident et le sauvegarde en base"""
    logger.info("📥 Nouvelle requête de prédiction")

    try:
        repository = AccidentRepository(session)
        service = AccidentService(repository)
        result = service.predict_and_save(data)

        logger.info(f"✅ Prédiction - ID: {result.id}, Gravité: {result.gravite_predite}")
        return result

    except Exception as e:
        logger.error(f"❌ Erreur: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/", response_model=List[Accident])
def get_accidents(session: SessionDep, pagination: PaginationDep):
    """Récupère la liste des accidents"""
    repository = AccidentRepository(session)
    service = AccidentService(repository)
    return service.get_all_accidents(**pagination)


@router.get("/{accident_id}", response_model=Accident)
def get_accident(accident_id: int, session: SessionDep):
    """Récupère un accident par ID"""
    try:
        repository = AccidentRepository(session)
        service = AccidentService(repository)
        return service.get_accident(accident_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
