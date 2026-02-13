# app/core/logging.py
"""Configuration centralisée du logging"""

import logging
import logging.handlers
import sys
from pathlib import Path

from app.core.config import settings

# Créer le dossier logs si nécessaire
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)


def setup_logging():
    """Configure le système de logging"""
    
    # Format des logs
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Niveau de log selon l'environnement
    log_level = logging.DEBUG if settings.ENV == "development" else logging.INFO
    
    # Configuration du logger racine
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        handlers=[
            # Console handler (stdout)
            logging.StreamHandler(sys.stdout),
            
            # File handler (fichier rotatif)
            logging.handlers.RotatingFileHandler(
                filename=LOGS_DIR / "app.log",
                maxBytes=10_000_000,  # 10MB
                backupCount=5,
                encoding="utf-8"
            )
        ]
    )
    
    # Configurer les loggers spécifiques
    
    # Logger pour uvicorn (moins verbeux)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    # Logger pour SQLAlchemy (moins verbeux)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)


# Logger principal de l'application
logger = logging.getLogger("accident_severity")