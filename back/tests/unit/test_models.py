"""
Tests unitaires pour les modèles.

Tests unitaires:
- Testent une unité de code isolée (classe, fonction)
- Pas de dépendances externes (DB, API, fichiers)
- Très rapides (millisecondes)
- Nombreux et spécifiques

Convention de nommage:
- Fichier: test_<module>.py
- Fonction: test_<what>_<when>_<expected>
"""

import pytest

from app.models.accident import Accident


class TestAccidentModel:
    """Tests pour le modèle Accident"""

    def test_accident_creation_with_all_fields(self, sample_accident_data):
        """
        Test: Créer un accident avec tous les champs
        Given: Données valides
        When: Création d'un Accident
        Then: L'objet est créé avec les bonnes valeurs
        """
        accident = Accident(**sample_accident_data, gravite_predite=1)

        assert accident.nb_usagers == 2
        assert accident.is_passagers == 0
        assert accident.age_cat == "25-44"
        assert accident.gravite_predite == 1

    def test_accident_creation_without_gravite(self, sample_accident_data):
        """
        Test: Créer un accident sans gravité prédite
        Given: Données sans gravite_predite
        When: Création d'un Accident
        Then: gravite_predite est None
        """
        accident = Accident(**sample_accident_data)

        assert accident.gravite_predite is None

    def test_accident_id_is_none_before_save(self, sample_accident_data):
        """
        Test: L'ID est None avant sauvegarde en DB
        Given: Accident créé en mémoire
        When: Avant l'ajout en DB
        Then: id est None
        """
        accident = Accident(**sample_accident_data)

        assert accident.id is None

    @pytest.mark.parametrize(
        "nb_usagers,expected",
        [
            (1, 1),
            (5, 5),
            (100, 100),
        ],
    )
    def test_accident_nb_usagers_values(self, sample_accident_data, nb_usagers, expected):
        """
        Test: Différentes valeurs de nb_usagers
        Given: Plusieurs valeurs possibles
        When: Création avec ces valeurs
        Then: La valeur est correctement stockée

        Parametrize permet de tester plusieurs cas en une seule fonction
        """
        data = {**sample_accident_data, "nb_usagers": nb_usagers}
        accident = Accident(**data)

        assert accident.nb_usagers == expected


# Pour lancer ces tests:
# $ pytest tests/unit/test_models.py
# $ pytest tests/unit/test_models.py::TestAccidentModel::test_accident_creation_with_all_fields
# $ pytest tests/unit/test_models.py -v
