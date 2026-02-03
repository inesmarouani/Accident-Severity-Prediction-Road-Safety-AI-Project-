from fastapi import FastAPI, status, Depends, HTTPException, Query, Request
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import Annotated, Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select


# =============================
# Modèle de données
# =============================

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


# =============================
# Initialisation
# =============================

app = FastAPI(title="Accident Severity API")

BASE_DIR = Path(__file__).resolve().parent

pipeline = joblib.load(BASE_DIR / "models/pipeline_binaire.pkl")
label_encoder = joblib.load(BASE_DIR / "models/label_encoder_binaire.pkl")


# =============================
# base de données
# =============================

# création de engine
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:////app/data/{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# Création de la table
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#creation d'un session de depandance
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


#Créer un BDD au démarrage
 
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# =============================
# CRUD
# =============================

#lire les accidents
@app.get("/accidents/")
def read_accidents(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Accident]:
    accidents = session.exec(select(Accident)).offset(offset).limit(limit).all()
    return accidents

#Lire un accident

@app.get("/accidents/{accident_id}")
def read_accident(accident_id: int, session: SessionDep) -> Accident:
    accident = session.get(Accident, accident_id)
    if not accident:
        raise HTTPException(status_code=404, detail="Accident not found")
    return accident




# =============================
# Prédiction (+ sauvegarde en BDD)
# =============================


@app.post("/predict", response_model=Accident)
def predict(data: AccidentInput, session: SessionDep):
    try:
        df = pd.DataFrame([data.model_dump()])

        # mettre l'ordre des colonnes attendu
        df = df[list(pipeline.feature_names_in_)]

        y_pred = pipeline.predict(df)
        gravite = int(y_pred[0])

         # Créer l'enregistrement avec le résultat
        accident = Accident(**data.model_dump(), gravite_predite=gravite)
        session.add(accident)
        session.commit()
        session.refresh(accident)

        return accident

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =============================
# Gestion des erreurs
# =============================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )


@app.get("/")
def root():
    return {"status": "API Accident Severity opérationnelle"}