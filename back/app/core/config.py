from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Accident Severity API"

    # Database
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "accidents"
    DB_HOST: str = "db"
    DB_PORT: str = "5432"

    # Environment
    ENV: str = "development"  # ← IMPORTANT

    # Models ML
    MODELS_PATH: Path = Path(__file__).resolve().parent.parent.parent / "models_trained"
    PIPELINE_FILE: str = "pipeline_binaire.pkl"
    LABEL_ENCODER_FILE: str = "label_encoder_binaire.pkl"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
