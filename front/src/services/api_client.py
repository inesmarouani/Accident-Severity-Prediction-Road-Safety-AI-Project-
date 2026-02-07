"""Client HTTP pour communiquer avec le backend"""

import requests
from src.config import config

class APIClient:
    """Client pour l'API Backend"""
    
    def __init__(self):
        self.base_url = config.API_BASE_URL
        self.timeout = 10
    
    def predict(self, payload: dict) -> dict:
        """
        Appelle l'endpoint de prédiction
        
        Args:
            payload: Données de l'accident
            
        Returns:
            dict: Réponse avec gravite_predite
            
        Raises:
            requests.HTTPError: Si erreur HTTP
        """
        response = requests.post(
            config.API_PREDICT_ENDPOINT,
            json=payload,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def get_accidents(self, offset: int = 0, limit: int = 100) -> list:
        """
        Récupère la liste des accidents
        
        Args:
            offset: Décalage
            limit: Limite
            
        Returns:
            list: Liste des accidents
        """
        params = {"offset": offset, "limit": limit}
        response = requests.get(
            config.API_ACCIDENTS_ENDPOINT,
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

# Instance singleton
api_client = APIClient()