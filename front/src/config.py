import os

class Config:
    """Configuration centralisée de l'application Dash"""
    
    # API Backend
    API_BASE_URL = os.getenv("API_BASE_URL", "http://backend:8000")
    API_PREDICT_ENDPOINT = f"{API_BASE_URL}/api/v1/accidents/predict"
    API_ACCIDENTS_ENDPOINT = f"{API_BASE_URL}/api/v1/accidents/"
    
    # Dash
    APP_HOST = "0.0.0.0"
    APP_PORT = 8050
    DEBUG = os.getenv("DEBUG", "False") == "True"
    
    # Data
    DATA_PATH = "data/accidents_clean.csv"
    
    # Style
    THEME = "FLATLY"  # Bootstrap theme

config = Config()