import logging
from typing import Optional

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from app.core.config import settings

logger = logging.getLogger(__name__)


class MLService:
    """Service pour les prédictions ML"""

    def __init__(self):
        self.pipeline: Optional[Pipeline] = None
        self.label_encoder: Optional[object] = None
        self._load_models()

    def _load_models(self) -> None:
        """Charge les modèles ML au démarrage"""
        logger.info("📦 Chargement des modèles ML...")

        pipeline_path = settings.MODELS_PATH / settings.PIPELINE_FILE
        encoder_path = settings.MODELS_PATH / settings.LABEL_ENCODER_FILE

        try:
            self.pipeline = joblib.load(pipeline_path)
            self.label_encoder = joblib.load(encoder_path)
            logger.info(f"✅ Modèles ML chargés depuis {settings.MODELS_PATH}")
        except Exception as e:
            logger.error(
                f"❌ Erreur lors du chargement des modèles: {e}", exc_info=True
            )
            raise

    def predict(self, data: dict) -> int:
        """Fait une prédiction de gravité d'accident"""

        if self.pipeline is None:
            raise RuntimeError("Pipeline ML non chargé")

        logger.debug(f"🔮 Prédiction pour: {data}")

        try:
            df = pd.DataFrame([data])
            df = df[list(self.pipeline.feature_names_in_)]

            y_pred = self.pipeline.predict(df)
            gravite = int(y_pred[0])

            logger.info(f"✅ Prédiction: {gravite}")
            return gravite

        except Exception as e:
            logger.error(f"❌ Erreur lors de la prédiction: {e}", exc_info=True)
            raise


ml_service = MLService()
