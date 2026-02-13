"""
Tests d'intégration pour l'API.

Tests d'intégration:
- Testent l'interaction entre plusieurs composants
- Incluent la DB, l'API, les services
- Plus lents que les tests unitaires
- Moins nombreux mais plus réalistes
"""


class TestPredictEndpoint:
    """Tests pour POST /api/v1/accidents/predict"""

    def test_predict_success(self, client, sample_accident_data):
        """
        Test: Prédiction réussie
        Given: Données valides
        When: POST /predict
        Then: 201 avec gravite_predite
        """
        response = client.post("/api/v1/accidents/predict", json=sample_accident_data)

        assert response.status_code == 201
        data = response.json()
        assert "gravite_predite" in data
        assert data["gravite_predite"] in [0, 1]
        assert "id" in data

    def test_predict_missing_field(self, client, sample_accident_data):
        """
        Test: Champ manquant
        Given: Données sans nb_usagers
        When: POST /predict
        Then: 422 Validation Error
        """
        incomplete_data = {**sample_accident_data}
        del incomplete_data["nb_usagers"]

        response = client.post("/api/v1/accidents/predict", json=incomplete_data)

        assert response.status_code == 422

    def test_predict_invalid_type(self, client, sample_accident_data):
        """
        Test: Type invalide
        Given: nb_usagers est string au lieu de int
        When: POST /predict
        Then: 422 Validation Error
        """
        invalid_data = {**sample_accident_data, "nb_usagers": "deux"}

        response = client.post("/api/v1/accidents/predict", json=invalid_data)

        assert response.status_code == 422


class TestGetAccidentsEndpoint:
    """Tests pour GET /api/v1/accidents/"""

    def test_get_accidents_empty(self, client):
        """
        Test: Récupérer accidents sur DB vide
        Given: Aucun accident en DB
        When: GET /accidents/
        Then: 200 avec liste vide
        """
        response = client.get("/api/v1/accidents/")

        assert response.status_code == 200
        assert response.json() == []

    def test_get_accidents_with_data(self, client, sample_accident_data):
        """
        Test: Récupérer accidents
        Given: 2 accidents en DB
        When: GET /accidents/
        Then: 200 avec 2 accidents
        """
        # Créer 2 accidents
        for _ in range(2):
            client.post("/api/v1/accidents/predict", json=sample_accident_data)

        response = client.get("/api/v1/accidents/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_accidents_pagination(self, client, sample_accident_data):
        """
        Test: Pagination
        Given: 5 accidents en DB
        When: GET /accidents/?offset=2&limit=2
        Then: 200 avec 2 accidents
        """
        # Créer 5 accidents
        for _ in range(5):
            client.post("/api/v1/accidents/predict", json=sample_accident_data)

        response = client.get("/api/v1/accidents/?offset=2&limit=2")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2


class TestGetAccidentByIdEndpoint:
    """Tests pour GET /api/v1/accidents/{id}"""

    def test_get_accident_success(self, client, sample_accident_data):
        """
        Test: Récupérer un accident existant
        Given: Accident en DB
        When: GET /accidents/{id}
        Then: 200 avec l'accident
        """
        # Créer un accident
        create_response = client.post(
            "/api/v1/accidents/predict", json=sample_accident_data
        )
        accident_id = create_response.json()["id"]

        # Récupérer l'accident
        response = client.get(f"/api/v1/accidents/{accident_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == accident_id

    def test_get_accident_not_found(self, client):
        """
        Test: Récupérer un accident inexistant
        Given: ID inexistant
        When: GET /accidents/99999
        Then: 404 Not Found
        """
        response = client.get("/api/v1/accidents/99999")

        assert response.status_code == 404


class TestHealthEndpoint:
    """Tests pour GET /health"""

    def test_health_check(self, client):
        """
        Test: Health check
        Given: Application démarrée
        When: GET /health
        Then: 200 avec status healthy
        """
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


# $ pytest tests/integration/test_api.py -v
# $ pytest tests/integration/test_api.py::TestPredictEndpoint -v
