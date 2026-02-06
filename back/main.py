from pathlib import Path
from typing import Annotated

import joblib
import pandas as pd
from database import SessionDep, create_db_and_tables
from fastapi import FastAPI, HTTPException, Query, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from models import Accident, AccidentInput
from sqlmodel import select

# =============================
# Initialisation
# =============================

app = FastAPI(title="Accident Severity API")

BASE_DIR = Path(__file__).resolve().parent

pipeline = joblib.load(BASE_DIR / "models_trained/pipeline_binaire.pkl")
label_encoder = joblib.load(BASE_DIR / "models_trained/label_encoder_binaire.pkl")

# =============================
# Startup
# =============================

#Créer un BDD au démarrage



#Créer un BDD au démarrage

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# =============================
# Gestion des erreurs
# =============================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )


# =============================
# Routes
# =============================

@app.get("/")
def root():
    return {"status": "API Accident Severity opérationnelle"}

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
        raise HTTPException(status_code=500, detail=str(e)) from e


#lire tous les accidents
@app.get("/accidents/")
def read_accidents(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Accident]:
    accidents = session.exec(select(Accident)).offset(offset).limit(limit).all()
    return accidents



#Lire un accident par ID

@app.get("/accidents/{accident_id}")
def read_accident(accident_id: int, session: SessionDep) -> Accident:
    accident = session.get(Accident, accident_id)
    if not accident:
        raise HTTPException(status_code=404, detail="Accident not found")
    return accident
