"""Tests unitaires pour les repositories"""

from app.models.accident import Accident
from app.repositories.accident_repository import AccidentRepository


class TestAccidentRepository:
    """Tests pour AccidentRepository"""

    def test_create_accident(self, session, sample_accident_data):
        """
        Test: Créer un accident via le repository
        Given: Session DB et données valides
        When: Appel à repo.create()
        Then: Accident créé avec un ID
        """
        repo = AccidentRepository(session)
        accident = Accident(**sample_accident_data, gravite_predite=0)

        created = repo.create(accident)

        assert created.id is not None
        assert created.nb_usagers == 2

    def test_get_by_id_existing(self, session, sample_accident):
        """
        Test: Récupérer un accident existant par ID
        Given: Accident déjà en DB
        When: Appel à repo.get_by_id()
        Then: Accident retourné
        """
        repo = AccidentRepository(session)

        found = repo.get_by_id(sample_accident.id)

        assert found is not None
        assert found.id == sample_accident.id

    def test_get_by_id_non_existing(self, session):
        """
        Test: Récupérer un accident inexistant
        Given: ID qui n'existe pas
        When: Appel à repo.get_by_id()
        Then: None retourné
        """
        repo = AccidentRepository(session)

        found = repo.get_by_id(99999)

        assert found is None

    def test_get_all_empty(self, session):
        """
        Test: get_all sur DB vide
        Given: Aucun accident en DB
        When: Appel à repo.get_all()
        Then: Liste vide retournée
        """
        repo = AccidentRepository(session)

        accidents = repo.get_all()

        assert len(accidents) == 0

    def test_get_all_with_data(self, session, sample_accident_data):
        """
        Test: get_all avec plusieurs accidents
        Given: 3 accidents en DB
        When: Appel à repo.get_all()
        Then: 3 accidents retournés
        """
        repo = AccidentRepository(session)

        # Créer 3 accidents
        for i in range(3):
            accident = Accident(**sample_accident_data, gravite_predite=i % 2)
            repo.create(accident)

        accidents = repo.get_all()

        assert len(accidents) == 3

    def test_get_all_with_pagination(self, session, sample_accident_data):
        """
        Test: Pagination de get_all
        Given: 5 accidents en DB
        When: Appel avec offset=2, limit=2
        Then: 2 accidents retournés (éléments 3 et 4)
        """
        repo = AccidentRepository(session)

        # Créer 5 accidents
        for _ in range(5):
            accident = Accident(**sample_accident_data, gravite_predite=0)
            repo.create(accident)

        accidents = repo.get_all(offset=2, limit=2)

        assert len(accidents) == 2


# $ pytest tests/unit/test_repositories.py -v
