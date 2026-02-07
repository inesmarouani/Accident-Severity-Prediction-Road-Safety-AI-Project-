from pydantic import BaseModel

class AccidentInput(BaseModel):
    """Schéma pour les données d'entrée de prédiction"""
    
    nb_usagers: int
    is_passagers: int
    age_cat: str
    nb_proteges: int
    trajet: float
    vma: float
    lum: float
    agg: int
    atm: float
    saison: str
    col: float
    situ: float
    circ: float
    localisation_pieton: int
    nbv: float

class AccidentResponse(BaseModel):
    """Schéma pour la réponse de prédiction"""
    
    id: int
    nb_usagers: int
    is_passagers: int
    age_cat: str
    nb_proteges: int
    trajet: float
    vma: float
    lum: float
    agg: int
    atm: float
    saison: str
    col: float
    situ: float
    circ: float
    localisation_pieton: int
    nbv: float
    gravite_predite: int | None