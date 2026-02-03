import os
from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends

from models import Accident  # importe le modèle pour que SQLModel le connaisse

# =============================
# Engine + connexion
# =============================

DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "accidents")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)


# =============================
# Création des tables
# =============================

# Création de la table
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#creation d'un session de depandance (dépendance FastAPI)
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


