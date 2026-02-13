"""
Connexion et gestion de la base de données.

Ce fichier centralise toute la logique de connexion DB.

Responsabilités:
- Création de l'engine SQLAlchemy
- Gestion des sessions
- Création des tables
- Utilitaires DB

Principe SOLID: Single Responsibility
Tout ce qui touche à la DB est ici, pas ailleurs.
"""

import logging
from collections.abc import Generator
from contextlib import contextmanager
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

logger = logging.getLogger(__name__)

# =============================
# ENGINE CONFIGURATION
# =============================

# L'engine est le point d'entrée SQLAlchemy vers la DB
# Il gère le pool de connexions, les transactions, etc.

engine_config = {
    "echo": settings.ENV == "development",  # Log SQL en dev
    "pool_pre_ping": True,  # Vérifie la connexion avant usage
    "pool_size": 5,  # Nombre de connexions dans le pool
    "max_overflow": 10,  # Connexions supplémentaires si besoin
}

# SQLite ne supporte pas pool_size/max_overflow
if settings.DATABASE_URL.startswith("sqlite"):
    engine_config = {"echo": settings.ENV == "development"}

engine = create_engine(settings.DATABASE_URL, **engine_config)

db_info = (
    settings.DATABASE_URL.split("@")[-1] if "@" in settings.DATABASE_URL else "SQLite"
)
logger.info(f"🗄️  Engine DB créé: {db_info}")


# =============================
# TABLE CREATION
# =============================


def create_db_and_tables():
    """
    Crée toutes les tables définies dans les modèles SQLModel.

    Appelé au démarrage de l'application (app.main.on_startup).

    Note: En production, utiliser Alembic pour les migrations
    au lieu de create_all() car:
    - Gestion de l'historique des changements
    - Rollback possible
    - Migrations versionées
    - Pas de perte de données

    Pour l'instant, create_all() suffit car:
    - Projet en développement
    - Pas de données en production
    - Schéma simple qui ne change pas souvent
    """
    logger.info("📋 Création des tables...")

    try:
        SQLModel.metadata.create_all(engine)
        logger.info("✅ Tables créées avec succès")
    except Exception as e:
        logger.error(f"❌ Erreur lors de la création des tables: {e}")
        raise


def drop_db_and_tables():
    """
    Supprime toutes les tables (DANGER - uniquement pour les tests).

    Usage:
        # Dans les tests
        def setup():
            drop_db_and_tables()
            create_db_and_tables()

    ⚠️ NE JAMAIS utiliser en production !
    """
    logger.warning("⚠️  SUPPRESSION de toutes les tables...")
    SQLModel.metadata.drop_all(engine)


# =============================
# SESSION MANAGEMENT
# =============================


def get_session() -> Generator[Session]:
    """
    Générateur de session pour FastAPI Dependency Injection.

    Lifecycle d'une session:
    1. Création: with Session(engine)
    2. Utilisation: dans l'endpoint
    3. Commit automatique: si pas d'erreur
    4. Rollback automatique: si erreur
    5. Fermeture: finally

    Exemple d'utilisation:
        @app.get("/accidents")
        def get_accidents(session: SessionDep):
            # session est créée ici
            accidents = session.exec(select(Accident)).all()
            # session.commit() automatique si pas d'erreur
            return accidents
            # session.close() automatique

    Avantages du pattern Generator:
    - try/finally garantit la fermeture
    - Gestion automatique des erreurs
    - Pas besoin de close() manuel
    """
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            # En cas d'erreur, rollback automatique
            session.rollback()
            logger.error(f"❌ Erreur DB, rollback: {e}")
            raise
        finally:
            # Toujours fermer la session
            session.close()


# Type annotation pour la dépendance FastAPI
# Utilise Annotated pour que l'IDE comprenne le type
SessionDep = Annotated[Session, Depends(get_session)]


# =============================
# CONTEXT MANAGER (optionnel)
# =============================


@contextmanager
def get_session_context() -> Generator[Session]:
    """
    Context manager pour usage hors FastAPI.

    Usage:
        # Dans un script CLI, cron job, etc.
        with get_session_context() as session:
            accidents = session.exec(select(Accident)).all()
            print(f"Total: {len(accidents)}")

    Différence avec get_session():
    - get_session(): pour FastAPI (Depends)
    - get_session_context(): pour scripts/CLI
    """
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Erreur: {e}")
            raise
        finally:
            session.close()


# =============================
# HEALTH CHECK
# =============================


def check_database_connection() -> bool:
    """
    Vérifie que la connexion DB fonctionne.

    Usage dans /health endpoint:
        @app.get("/health")
        def health():
            db_ok = check_database_connection()
            return {
                "status": "healthy" if db_ok else "unhealthy",
                "database": "connected" if db_ok else "disconnected"
            }

    Utile pour:
    - Kubernetes liveness/readiness probes
    - Monitoring (Prometheus, Datadog)
    - Debugging
    """
    try:
        with Session(engine) as session:
            # Execute une requête simple
            session.exec("SELECT 1")  # type: ignore[call-overload]
        return True
    except Exception as e:
        logger.error(f"❌ DB Health Check failed: {e}")
        return False


# =============================
# NOTES IMPORTANTES
# =============================

"""
Pool de connexions:
- pool_size=5: 5 connexions permanentes
- max_overflow=10: jusqu'à 15 connexions au total si nécessaire
- pool_pre_ping=True: vérifie que la connexion est vivante avant usage

Pourquoi c'est important:
- Évite "connection already closed" errors
- Meilleure performance (réutilisation des connexions)
- Limite la charge sur la DB

Sessions vs Connexions:
- Session: unité de travail (transaction)
- Connection: lien TCP vers la DB
- Une session utilise une connection du pool

Best practices:
1. Toujours fermer les sessions (with ou try/finally)
2. Ne jamais partager une session entre threads
3. Garder les sessions courtes (pas de state entre requêtes)
4. Utiliser des transactions explicites si besoin de cohérence

Migrations (pour plus tard):
$ pip install alembic
$ alembic init migrations
$ alembic revision --autogenerate -m "Initial migration"
$ alembic upgrade head

Voir: https://alembic.sqlalchemy.org/
"""
