from sqlmodel import Field, SQLModel
from typing import Optional
from pydantic import BaseModel


# Schéma des données d'entrée
class AccidentInput(BaseModel):
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
    situ : float
    circ: float
    localisation_pieton: int
    nbv : float


# Modèle SQLModel : table DB + schéma de retour
class Accident(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # clé primaire
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
    situ : float
    circ: float
    localisation_pieton: int
    nbv : float
    gravite_predite: Optional[int] = None  # résultat de la prédiction
