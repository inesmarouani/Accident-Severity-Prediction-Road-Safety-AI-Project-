"""Constantes et options pour les dropdowns"""

OPTIONS = {
    "is_passagers": [{"label": "Non", "value": 0}, {"label": "Oui", "value": 1}],
    "col": [
        {"label": "Deux véhicules - frontale", "value": 1},
        {"label": "Deux véhicules – par l'arrière", "value": 2},
        {"label": "Deux véhicules – par le coté", "value": 3},
        {"label": "Trois véhicules et plus – en chaîne", "value": 4},
        {"label": "Trois véhicules et plus - collisions multiples", "value": 5},
        {"label": "Autre collision", "value": 6},
        {"label": "Sans collision", "value": 7},
    ],
    "age_cat": [
        {"label": "0-2", "value": "0-2"},
        {"label": "3-11", "value": "3-11"},
        {"label": "12-17", "value": "12-17"},
        {"label": "18-64", "value": "18-64"},
        {"label": "65+", "value": "65+"},
    ],
    "trajet": [
        {"label": "Non renseigné", "value": 0},
        {"label": "Domicile – travail", "value": 1},
        {"label": "Domicile – école", "value": 2},
        {"label": "Courses – achats", "value": 3},
        {"label": "Utilisation professionnelle", "value": 4},
        {"label": "Promenade – loisirs", "value": 5},
        {"label": "Autre", "value": 9},
    ],
    "circ": [
        {"label": "A sens unique", "value": 1},
        {"label": "Bidirectionnelle", "value": 2},
        {"label": "A chaussées séparées", "value": 3},
        {"label": "Avec voies d'affectation variable", "value": 4},
    ],
    "lum": [
        {"label": "Plein jour", "value": 1},
        {"label": "Crépuscule ou aube", "value": 2},
        {"label": "Nuit sans éclairage public", "value": 3},
        {"label": "Nuit avec éclairage public non allumé", "value": 4},
        {"label": "Nuit avec éclairage public allumé", "value": 5},
    ],
    "agg": [{"label": "Hors agglomération", "value": 1}, {"label": "En agglomération", "value": 2}],
    "atm": [
        {"label": "Normale", "value": 1},
        {"label": "Pluie légère", "value": 2},
        {"label": "Pluie forte", "value": 3},
        {"label": "Neige - grêle", "value": 4},
        {"label": "Brouillard - fumée", "value": 5},
        {"label": "Vent fort - tempête", "value": 6},
        {"label": "Temps éblouissant", "value": 7},
        {"label": "Temps couvert", "value": 8},
        {"label": "Autre", "value": 9},
    ],
    "situ": [
        {"label": "Aucun", "value": 0},
        {"label": "Sur chaussée", "value": 1},
        {"label": "Sur bande d'arrêt d'urgence", "value": 2},
        {"label": "Sur accotement", "value": 3},
        {"label": "Sur trottoir", "value": 4},
        {"label": "Sur piste cyclable", "value": 5},
        {"label": "Sur autre voie spéciale", "value": 6},
        {"label": "Temps éblouissant", "value": 7},
        {"label": "Autres", "value": 8},
    ],
    "localisation_pieton": [
        {"label": "Sur chaussée", "value": 1},
        {"label": "Sur passage piéton", "value": 2},
        {"label": "Autre", "value": 3},
    ],
    "saison": [
        {"label": "été", "value": "ete"},
        {"label": "automne", "value": "automne"},
        {"label": "hiver", "value": "hiver"},
        {"label": "printemps", "value": "printemps"},
    ],
}

GRAVITE_LABELS = {
    0: "🟢 Accident sans blessé grave",
    1: "🔴 Accident avec blessés graves/mortel",
}

GRAVITE_COLORS = {0: "success", 1: "warning"}
