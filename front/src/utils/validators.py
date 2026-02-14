"""Validation des données d'entrée"""


def to_flag(val):
    """
    Convertit une valeur de checklist en 0/1

    Args:
        val: Valeur à convertir (list, int, str, bool)

    Returns:
        int: 0 ou 1
    """
    if isinstance(val, list):
        return 1 if 1 in val else 0
    if val in (1, "1", True):
        return 1
    return 0


def validate_prediction_data(data: dict) -> tuple[bool, str]:
    """
    Valide les données de prédiction

    Args:
        data: Dictionnaire des données

    Returns:
        tuple: (is_valid, error_message)
    """
    required = [
        "nb_proteges",
        "nbv",
        "vma",
        "lum",
        "saison",
        "localisation_pieton",
        "trajet",
        "age_cat",
        "is_passagers",
        "circ",
        "nb_usagers",
        "atm",
        "agg",
        "col",
        "situ",
    ]

    for field in required:
        if field not in data or data[field] is None:
            return False, f"Le champ '{field}' est requis"

    return True, ""
