from locust import HttpUser, between, task


class CRUDUser(HttpUser):
    """Profil utilisateur CRUD complet"""

    wait_time = between(1, 3)
    weight = 1

    @task(3)
    def get_accidents(self):
        """Lecture de tous les accidents"""
        self.client.get("/api/v1/accidents/")

    @task(2)
    def get_accident_by_id(self):
        """Lecture d'un accident par ID"""
        self.client.get("/api/v1/accidents/1")

    @task(5)
    def predict_accident(self):
        """Création d'une prédiction"""
        self.client.post(
            "/api/v1/accidents/predict",
            json={
                "nb_usagers": 2,
                "is_passagers": 1,
                "age_cat": "adulte",
                "nb_proteges": 1,
                "trajet": 1.0,
                "vma": 50.0,
                "lum": 1.0,
                "agg": 1,
                "atm": 1.0,
                "saison": "ete",
                "col": 3.0,
                "situ": 1.0,
                "circ": 2.0,
                "localisation_pieton": 0,
                "nbv": 2.0,
            },
        )

    @task(1)
    def health_check(self):
        """Vérification santé API"""
        self.client.get("/health")


class ReadOnlyUser(HttpUser):
    """Profil utilisateur lecture seule"""

    wait_time = between(0.5, 2)
    weight = 3

    @task(5)
    def get_accidents(self):
        """Lecture de tous les accidents"""
        self.client.get("/api/v1/accidents/")

    @task(3)
    def get_accident_by_id(self):
        """Lecture d'un accident par ID"""
        self.client.get("/api/v1/accidents/1")

    @task(2)
    def health_check(self):
        """Vérification santé API"""
        self.client.get("/health")
