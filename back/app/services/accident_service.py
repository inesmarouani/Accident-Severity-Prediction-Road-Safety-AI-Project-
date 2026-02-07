from app.models.accident import Accident
from app.schemas.accident import AccidentInput
from app.repositories.accident_repository import AccidentRepository
from app.services.ml_service import ml_service

class AccidentService:
    """Service métier pour la gestion des accidents"""
    
    def __init__(self, repository: AccidentRepository):
        self.repository = repository
    
    def predict_and_save(self, data: AccidentInput) -> Accident:
        """
        Prédit la gravité et sauvegarde l'accident
        
        Args:
            data: Données d'entrée de l'accident
            
        Returns:
            Accident: Accident avec la prédiction
        """
        # Prédiction
        gravite = ml_service.predict(data.model_dump())
        
        # Créer l'objet Accident
        accident = Accident(**data.model_dump(), gravite_predite=gravite)
        
        # Sauvegarder
        return self.repository.create(accident)
    
    def get_accident(self, accident_id: int) -> Accident:
        """Récupère un accident par ID"""
        accident = self.repository.get_by_id(accident_id)
        if not accident:
            raise ValueError(f"Accident {accident_id} not found")
        return accident
    
    def get_all_accidents(self, offset: int = 0, limit: int = 100) -> list[Accident]:
        """Récupère tous les accidents"""
        return self.repository.get_all(offset, limit)