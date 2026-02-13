from sqlmodel import Session

from app.models.accident import Accident
from app.repositories.base import BaseRepository


class AccidentRepository(BaseRepository[Accident]):
    """Repository pour l'accès aux données des accidents"""
    
    def __init__(self, session: Session):
        super().__init__(Accident, session)