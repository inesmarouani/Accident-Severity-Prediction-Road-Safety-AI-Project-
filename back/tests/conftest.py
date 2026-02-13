"""
Configuration globale pour pytest.

conftest.py est un fichier spécial de pytest qui:
- Définit des fixtures réutilisables
- Configure l'environnement de test
- Est automatiquement découvert par pytest

Fixtures pytest:
- Fonctions décorées avec @pytest.fixture
- Injectées automatiquement dans les tests
- Gèrent le setup/teardown automatiquement
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database import get_session
from app.main import app

# =============================
# DATABASE FIXTURES
# =============================


@pytest.fixture(name="session")
def session_fixture():
    """
    Crée une session DB en mémoire pour les tests.

    Utilise SQLite in-memory (très rapide):
    - Créée avant chaque test
    - Supprimée après chaque test
    - Isolation complète entre tests

    Usage dans un test:
        def test_create_accident(session):
            accident = Accident(nb_usagers=2, ...)
            session.add(accident)
            session.commit()
            assert accident.id is not None
    """
    # Engine SQLite en mémoire
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Créer toutes les tables
    SQLModel.metadata.create_all(engine)

    # Créer la session
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()

    # Cleanup: supprimer les tables après le test
    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Client de test FastAPI avec DB mocké.

    Override la dépendance get_session pour utiliser
    notre session de test au lieu de la vraie DB.

    Usage:
        def test_predict_endpoint(client):
            response = client.post("/api/v1/accidents/predict", json={...})
            assert response.status_code == 201
    """

    def get_session_override():
        return session

    # Override la dépendance
    app.dependency_overrides[get_session] = get_session_override

    # Créer le client de test
    client = TestClient(app)
    yield client

    # Cleanup: retirer l'override
    app.dependency_overrides.clear()


# =============================
# DATA FIXTURES
# =============================


@pytest.fixture
def sample_accident_data():
    """
    Données d'exemple pour créer un accident.

    Usage:
        def test_something(sample_accident_data):
            accident = Accident(**sample_accident_data)
    """
    return {
        "nb_usagers": 2,
        "is_passagers": 0,
        "age_cat": "25-44",
        "nb_proteges": 1,
        "trajet": 1.0,
        "vma": 50.0,
        "lum": 1.0,
        "agg": 1,
        "atm": 1.0,
        "saison": "printemps",
        "col": 2.0,
        "situ": 1.0,
        "circ": 2.0,
        "localisation_pieton": 0,
        "nbv": 2.0,
    }


@pytest.fixture
def sample_accident(session: Session, sample_accident_data):
    """
    Crée un accident en DB pour les tests.

    Usage:
        def test_get_accident(client, sample_accident):
            response = client.get(f"/api/v1/accidents/{sample_accident.id}")
            assert response.status_code == 200
    """
    from app.models.accident import Accident

    accident = Accident(**sample_accident_data, gravite_predite=0)
    session.add(accident)
    session.commit()
    session.refresh(accident)

    return accident


# =============================
# CONFIGURATION PYTEST
# =============================


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Setup global pour tous les tests.

    scope="session": exécuté une seule fois pour toute la suite de tests
    autouse=True: exécuté automatiquement sans être demandé

    Utilisé pour:
    - Configurer les variables d'environnement
    - Initialiser les mocks globaux
    - Configurer le logging
    """
    import os

    # Forcer l'environnement de test
    os.environ["ENV"] = "test"
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"

    yield

    # Cleanup après tous les tests
    pass


# =============================
# MARKERS PYTEST
# =============================

"""
Markers personnalisés pour organiser les tests.

Définir dans pytest.ini ou pyproject.toml:

[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]

Usage:
    @pytest.mark.slow
    def test_something_slow():
        ...

    @pytest.mark.integration
    def test_api_endpoint():
        ...

Lancer seulement les tests unitaires:
$ pytest -m unit

Exclure les tests lents:
$ pytest -m "not slow"
"""


# =============================
# EXAMPLE TESTS
# =============================

"""
Exemples de structure de tests (à créer dans tests/unit/ et tests/integration/)

tests/unit/test_models.py:
    def test_accident_creation(sample_accident_data):
        accident = Accident(**sample_accident_data)
        assert accident.nb_usagers == 2

tests/unit/test_repositories.py:
    def test_accident_repository_create(session, sample_accident_data):
        repo = AccidentRepository(session)
        accident = Accident(**sample_accident_data, gravite_predite=0)
        created = repo.create(accident)
        assert created.id is not None

tests/unit/test_services.py:
    def test_ml_service_predict(sample_accident_data):
        from app.services.ml_service import ml_service
        gravite = ml_service.predict(sample_accident_data)
        assert gravite in [0, 1]

tests/integration/test_api.py:
    def test_predict_endpoint(client, sample_accident_data):
        response = client.post("/api/v1/accidents/predict", json=sample_accident_data)
        assert response.status_code == 201
        assert "gravite_predite" in response.json()

Lancer les tests:
$ pytest                          # Tous les tests
$ pytest tests/unit/              # Tests unitaires seulement
$ pytest tests/integration/       # Tests d'intégration seulement
$ pytest -v                       # Mode verbose
$ pytest --cov=app --cov-report=html  # Avec couverture de code
"""
