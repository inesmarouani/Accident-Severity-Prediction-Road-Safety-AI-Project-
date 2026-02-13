# app/services/ml_service.py
import joblib
import pandas as pd
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class MLService:
    """Service pour les prédictions ML"""
    
    def __init__(self):
        self.pipeline = None
        self.label_encoder = None
        self._load_models()
    
    def _load_models(self):
        """Charge les modèles ML au démarrage"""
        logger.info("📦 Chargement des modèles ML...")
        
        pipeline_path = settings.MODELS_PATH / settings.PIPELINE_FILE
        encoder_path = settings.MODELS_PATH / settings.LABEL_ENCODER_FILE
        
        try:
            self.pipeline = joblib.load(pipeline_path)
            self.label_encoder = joblib.load(encoder_path)
            logger.info(f"✅ Modèles ML chargés depuis {settings.MODELS_PATH}")
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement des modèles: {e}", exc_info=True)
            raise
    
    def predict(self, data: dict) -> int:
        """Fait une prédiction de gravité d'accident"""
        logger.debug(f"🔮 Prédiction pour: {data}")
        
        try:
            df = pd.DataFrame([data])
            df = df[list(self.pipeline.feature_names_in_)]  # type: ignore[union-attr]
            
            y_pred = self.pipeline.predict(df)  # type: ignore[union-attr]
            gravite = int(y_pred[0])
            
            logger.info(f"✅ Prédiction: {gravite}")
            return gravite
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la prédiction: {e}", exc_info=True)
            raise

ml_service = MLService()