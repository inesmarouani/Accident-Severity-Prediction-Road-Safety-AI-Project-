"""
Point d'entrée simple pour la configuration.

Ce fichier sert de "façade" pour accéder à la configuration.
Au lieu d'importer depuis app.core.config partout, on importe depuis app.config.

Avantages:
- Imports plus courts: from app.config import settings
- Abstraction: on peut changer l'implémentation de config sans toucher au code
- Convention: config à la racine comme database, main, etc.

Pattern de conception: Facade Pattern
Simplifie l'accès à un sous-système complexe (core.config)
"""

from app.core.config import settings

__all__ = ["settings"]

# Note: Ce fichier peut sembler inutile maintenant, mais il permet:
# 1. Une structure cohérente (config.py au même niveau que database.py)
# 2. D'ajouter des configurations dérivées facilement:
#
# def get_database_url_for_env(env: str) -> str:
#     """Retourne l'URL DB selon l'environnement"""
#     if env == "test":
#         return "sqlite:///./test.db"
#     return settings.DATABASE_URL
