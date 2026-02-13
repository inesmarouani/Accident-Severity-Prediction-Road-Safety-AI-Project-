"""
Dépendances communes pour les endpoints API.

Les dépendances FastAPI permettent:
- Réutilisation du code (DRY)
- Injection automatique
- Validation centralisée
- Meilleure testabilité

Concept clé: Dependency Injection
Au lieu de créer des objets manuellement dans chaque endpoint,
FastAPI les injecte automatiquement.
"""

from typing import Annotated, Generator
from fastapi import Depends, HTTPException, Header, Query, status
from sqlmodel import Session
from app.database import get_session

# =============================
# DÉPENDANCE: Session DB
# =============================

SessionDep = Annotated[Session, Depends(get_session)]

"""
Usage dans un endpoint:
    @app.get("/accidents")
    def get_accidents(session: SessionDep):
        # session est automatiquement créée et fermée
        accidents = session.exec(select(Accident)).all()
        return accidents

Avantages:
- Pas besoin de faire session.close() manuellement
- Gestion automatique des transactions
- Facile à mocker dans les tests
"""


# =============================
# DÉPENDANCE: Pagination
# =============================


def get_pagination_params(
    offset: int = Query(default=0, ge=0, description="Nombre d'éléments à sauter"),
    limit: int = Query(default=100, ge=1, le=100, description="Nombre max d'éléments"),
) -> dict:
    """
    Paramètres de pagination réutilisables.

    Validation automatique:
    - offset >= 0 (pas de valeurs négatives)
    - 1 <= limit <= 100 (max 100 éléments par page)

    Usage:
        @app.get("/accidents")
        def get_accidents(pagination: PaginationDep):
            offset = pagination["offset"]
            limit = pagination["limit"]

    Exemples de requêtes:
    - /accidents                    → offset=0, limit=100 (défaut)
    - /accidents?offset=50&limit=25 → offset=50, limit=25
    - /accidents?limit=200          → Erreur 422 (limit > 100)
    """
    return {"offset": offset, "limit": limit}


PaginationDep = Annotated[dict, Depends(get_pagination_params)]


# =============================
# DÉPENDANCE: API Key (optionnel)
# =============================


async def verify_api_key(
    api_key: str = Header(None, alias="X-API-Key", description="Clé API pour l'authentification"),
) -> str:
    """
    Vérifie la validité d'une API key (optionnel - non utilisé actuellement).

    Usage futur pour sécuriser l'API:
        @app.post("/predict", dependencies=[Depends(verify_api_key)])
        def predict(...):
            # Accessible uniquement avec une clé valide

    Headers de requête:
        X-API-Key: votre_cle_secrete_ici

    TODO: Implémenter la vérification avec une vraie DB de clés
    """
    if api_key is None:
        # Pour l'instant, on n'exige pas de clé
        return None

    # Exemple de validation (à remplacer par DB)
    valid_keys = ["dev_key_12345", "prod_key_67890"]

    if api_key not in valid_keys:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")

    return api_key


# =============================
# DÉPENDANCE: Rate Limiting (optionnel)
# =============================


class RateLimiter:
    """
    Limite le nombre de requêtes par utilisateur/IP.

    Exemple d'usage futur:
        @app.post("/predict", dependencies=[Depends(RateLimiter(max_calls=100, period=3600))])
        def predict(...):
            # Max 100 prédictions par heure

    TODO: Implémenter avec Redis ou slowapi
    Voir: https://github.com/laurentS/slowapi
    """

    def __init__(self, max_calls: int, period: int):
        """
        Args:
            max_calls: Nombre max d'appels autorisés
            period: Période en secondes
        """
        self.max_calls = max_calls
        self.period = period

    async def __call__(self, request):
        # TODO: Implémenter la logique de rate limiting
        pass


# =============================
# DÉPENDANCE: Current User (pour auth future)
# =============================


async def get_current_user(
    token: str = Depends(),  # TODO: OAuth2PasswordBearer
) -> dict:
    """
    Récupère l'utilisateur actuel depuis le token JWT.

    Usage futur avec authentification:
        @app.get("/me")
        def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
            return current_user

    TODO: Implémenter avec python-jose pour JWT
    Voir: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
    """
    # Placeholder
    return {"username": "anonymous"}


# Note: Pour une vraie API en production, implémenter:
# 1. Rate limiting (slowapi, redis)
# 2. API keys en DB
# 3. JWT avec refresh tokens
# 4. Logging des accès
# 5. CORS selon vos besoins
