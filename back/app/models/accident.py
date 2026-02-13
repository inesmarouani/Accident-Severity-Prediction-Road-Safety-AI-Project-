from typing import Optional
from sqlmodel import Field, SQLModel
from app.models.base import TimestampMixin


class Accident(TimestampMixin, table=True):
    """Modèle de la table accidents en base de données"""

    __tablename__ = "accidents"

    id: Optional[int] = Field(default=None, primary_key=True)
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
    gravite_predite: Optional[int] = None
