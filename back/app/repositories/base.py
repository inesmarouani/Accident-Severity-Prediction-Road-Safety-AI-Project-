"""
Repository de base avec opérations CRUD génériques.

Le pattern Repository sépare la logique d'accès aux données
de la logique métier.

Avantages:
- Testabilité: facile de mocker un repository
- Réutilisabilité: CRUD générique pour tous les modèles
- Changement de DB: un seul endroit à modifier
- Cohérence: toutes les opérations au même endroit

Architecture:
    Controller (API endpoint)
        ↓
    Service (logique métier)
        ↓
    Repository (accès données)
        ↓
    Database
"""

from typing import TypeVar

from sqlmodel import Session, SQLModel, col, select

# TypeVar permet de créer des génériques type-safe
# Exemple: BaseRepository[Accident] garantit que toutes les méthodes
# retournent des objets Accident
ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository[ModelType]:
    """
    Repository de base avec opérations CRUD.

    CRUD = Create, Read, Update, Delete

    Usage:
        class UserRepository(BaseRepository[User]):
            def __init__(self, session: Session):
                super().__init__(User, session)

            # Ajouter des méthodes spécifiques:
            def get_by_email(self, email: str):
                ...
    """

    def __init__(self, model: type[ModelType], session: Session):
        """
        Args:
            model: La classe du modèle (ex: Accident, User)
            session: Session SQLModel pour les requêtes
        """
        self.model = model
        self.session = session

    def create(self, obj: ModelType) -> ModelType:
        """
        Créer un nouvel objet en base de données.

        Args:
            obj: Instance du modèle à créer

        Returns:
            L'objet créé avec son ID généré

        Exemple:
            accident = Accident(nb_usagers=2, ...)
            saved = repo.create(accident)
            print(saved.id)  # ID auto-généré
        """
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)  # Recharger depuis la DB pour avoir l'ID
        return obj

    def get_by_id(self, obj_id: int) -> ModelType | None:
        """
        Récupérer un objet par son ID.

        Returns:
            L'objet si trouvé, None sinon

        Exemple:
            accident = repo.get_by_id(42)
            if accident:
                print(accident.gravite_predite)
        """
        return self.session.get(self.model, obj_id)

    def get_all(self, offset: int = 0, limit: int = 100) -> list[ModelType]:
        """
        Récupérer tous les objets avec pagination.

        Pagination nécessaire pour éviter de charger des millions
        d'enregistrements en mémoire.

        Args:
            offset: Nombre d'éléments à sauter (pour la page)
            limit: Nombre max d'éléments à retourner

        Exemple:
            # Page 1 (premiers 100)
            page1 = repo.get_all(offset=0, limit=100)

            # Page 2 (éléments 100-200)
            page2 = repo.get_all(offset=100, limit=100)
        """
        statement = select(self.model).offset(offset).limit(limit)
        return list(self.session.exec(statement).all())

    def update(self, obj: ModelType) -> ModelType:
        """
        Mettre à jour un objet existant.

        Note: SQLModel détecte automatiquement les changements

        Exemple:
            accident = repo.get_by_id(42)
            accident.gravite_predite = 1
            updated = repo.update(accident)
        """
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, obj: ModelType) -> None:
        """
        Supprimer un objet (suppression physique).

        Pour soft delete, utiliser SoftDeleteMixin à la place.

        Exemple:
            accident = repo.get_by_id(42)
            repo.delete(accident)
        """
        self.session.delete(obj)
        self.session.commit()

    def count(self) -> int:
        """
        Compter le nombre total d'enregistrements.

        Utile pour la pagination (nombre total de pages).

        Exemple:
            total = repo.count()
            pages = (total + limit - 1) // limit
        """
        statement = select(col(self.model.id)).select_from(self.model)  # type: ignore[attr-defined]
        return len(list(self.session.exec(statement).all()))

    def exists(self, obj_id: int) -> bool:
        """
        Vérifie si un objet existe.

        Plus rapide que get_by_id car ne charge pas l'objet.

        Exemple:
            if repo.exists(42):
                print("L'accident 42 existe")
        """
        return self.get_by_id(obj_id) is not None


# Note sur les performances:
# - Toujours utiliser pagination sur de gros datasets
# - Ajouter des index sur les colonnes fréquemment recherchées
# - Utiliser select() au lieu de .all() pour lazy loading
# - Faire attention aux N+1 queries (jointures)
