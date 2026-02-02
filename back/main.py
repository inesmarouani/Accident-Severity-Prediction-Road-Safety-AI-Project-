from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import pandas as pd
from pathlib import Path
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import status

# =============================
# Initialisation
# =============================

app = FastAPI(title="Accident Severity API")

BASE_DIR = Path(__file__).resolve().parent

pipeline = joblib.load(BASE_DIR / "models/pipeline_binaire.pkl")
label_encoder = joblib.load(BASE_DIR / "models/label_encoder_binaire.pkl")

# =============================
# Schéma des données d'entrée
# =============================

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



# =============================
# Routes
# =============================


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )



@app.get("/")
def root():
    return {"status": "API Accident Severity opérationnelle"}


@app.post("/predict")
def predict(data: AccidentInput):
    try:
        df = pd.DataFrame([data.dict()])

        # mettre l'ordre des colonnes attendu
        df = df[list(pipeline.feature_names_in_)]

        y_pred = pipeline.predict(df)
        return {"gravite_predite": int(y_pred[0])}

    except Exception as e:
        raise e

