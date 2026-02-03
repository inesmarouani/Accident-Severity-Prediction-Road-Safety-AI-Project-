from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends

from models import Accident  # importe le modèle pour que SQLModel le connaisse

# =============================
# Engine + connexion
# =============================
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:////app/data/{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


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


