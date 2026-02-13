"""
Modèles de base pour SQLModel.

Ce fichier définit des classes de base réutilisables pour tous les modèles.
Principe DRY (Don't Repeat Yourself): éviter de dupliquer le code.

Concepts:
- Mixin: classe qui ajoute des fonctionnalités à d'autres classes
- Héritage multiple: une classe peut hériter de plusieurs mixins
- Timestamps automatiques: created_at/updated_at gérés par la DB
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class TimestampMixin(SQLModel):
    """
    Mixin pour ajouter created_at et updated_at à tous les modèles.
    
    Usage:
        class MyModel(TimestampMixin, table=True):
            id: int
            name: str
            # created_at et updated_at sont ajoutés automatiquement
    
    Avantages:
    - Traçabilité: savoir quand un enregistrement a été créé/modifié
    - Audit: suivre l'historique des modifications
    - Debug: identifier les problèmes temporels
    
    Note: Non utilisé pour Accident car pas nécessaire pour des prédictions,
    mais utile pour User, Log, etc.
    """
    
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Date de création de l'enregistrement"
    )
    
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        description="Date de dernière modification"
    )


class SoftDeleteMixin(SQLModel):
    """
    Mixin pour la suppression logique (soft delete).
    
    Au lieu de supprimer vraiment un enregistrement (DELETE),
    on le marque comme supprimé (UPDATE deleted_at = NOW()).
    
    Avantages:
    - Récupération possible si erreur
    - Historique complet
    - Conformité RGPD (garder trace des suppressions)
    
    Usage:
        class MyModel(SoftDeleteMixin, table=True):
            # Filtrer les non-supprimés:
            # SELECT * FROM mymodel WHERE deleted_at IS NULL
    """
    
    deleted_at: Optional[datetime] = Field(
        default=None,
        nullable=True,
        description="Date de suppression (NULL si actif)"
    )
    
    def is_deleted(self) -> bool:
        """Vérifie si l'enregistrement est supprimé"""
        return self.deleted_at is not None
    
    def soft_delete(self):
        """Marque l'enregistrement comme supprimé"""
        self.deleted_at = datetime.utcnow()


class BaseModel(SQLModel):
    """
    Classe de base pour tous les modèles.
    
    Pour l'instant vide, mais pourrait contenir:
    - Méthodes communes (to_dict, from_dict)
    - Validations communes
    - Métadonnées partagées
    
    Usage:
        class MyModel(BaseModel, table=True):
            id: int
            name: str
    """
    pass


# Exemple d'utilisation complète (pour référence):
"""
class User(TimestampMixin, SoftDeleteMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = True
    # Hérite automatiquement de:
    # - created_at
    # - updated_at  
    # - deleted_at
    # - is_deleted()
    # - soft_delete()
"""