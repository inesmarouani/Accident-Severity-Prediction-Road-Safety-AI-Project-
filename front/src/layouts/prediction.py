"""Layout de la page de prédiction"""

import dash_bootstrap_components as dbc
from dash import dcc, html

from src.utils.constants import OPTIONS


def create_prediction_layout():
    """Crée le layout de la page de prédiction"""

    return dbc.Card(
        [
            dbc.CardHeader("🔮 Prédiction de la gravité"),
            dbc.CardBody(
                [
                    # GENERAL
                    html.H5("Informations générales"),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label("Nb usagers"),
                                    dbc.Input(id="nb_usagers", type="number", value=1, min=1),
                                ],
                                md=3,
                            ),
                            dbc.Col(
                                [
                                    html.Label("Nb protégés"),
                                    dbc.Input(id="nb_proteges", type="number", value=0),
                                ],
                                md=3,
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Hr(),
                    # PROFIL
                    html.H5("Profil des usagers"),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label("Passager ?"),
                                    dbc.Checklist(
                                        id="is_passagers",
                                        options=[{"label": "Oui", "value": 1}],
                                        value=[],
                                    ),
                                ],
                                md=3,
                            ),
                            dbc.Col(
                                [
                                    html.Label("Catégorie d'âge"),
                                    dcc.Dropdown(
                                        id="age_cat",
                                        options=OPTIONS["age_cat"],
                                        placeholder="Sélectionner",
                                    ),
                                ],
                                md=3,
                            ),
                            dbc.Col(
                                [
                                    html.Label("Trajet"),
                                    dcc.Dropdown(
                                        id="trajet",
                                        options=OPTIONS["trajet"],
                                        placeholder="Sélectionner",
                                    ),
                                ],
                                md=3,
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Hr(),
                    # CIRCULATION
                    html.H5("Conditions de circulation"),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label("Agglomération ?"),
                                    dbc.Checklist(
                                        id="agg", options=[{"label": "Oui", "value": 1}], value=[]
                                    ),
                                ],
                                md=3,
                            ),
                            dbc.Col(
                                [
                                    html.Label("Type de circulation"),
                                    dcc.Dropdown(
                                        id="circ",
                                        options=OPTIONS["circ"],
                                        placeholder="Sélectionner",
                                    ),
                                ],
                                md=3,
                            ),
                            dbc.Col(
                                [
                                    html.Label("VMA (km/h)"),
                                    dbc.Input(id="vma", type="number", value=50, min=10, step=10),
                                ],
                                md=3,
                            ),
                            dbc.Col(
                                [
                                    html.Label("Nombre de véhicules"),
                                    dbc.Input(id="nbv", type="number", value=1, min=1, step=1),
                                ],
                                md=3,
                            ),
                        ],
                        className="mb-3",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label("Localisation des piétons"),
                                    dcc.Dropdown(
                                        id="localisation_pieton",
                                        options=OPTIONS["localisation_pieton"],
                                        placeholder="Sélectionner",
                                    ),
                                ],
                                md=3,
                            ),
                            dbc.Col(
                                [
                                    html.Label("Luminosité"),
                                    dcc.Dropdown(
                                        id="lum", options=OPTIONS["lum"], placeholder="Sélectionner"
                                    ),
                                ],
                                md=3,
                            ),
                            dbc.Col(
                                [
                                    html.Label("Conditions atmosphériques"),
                                    dcc.Dropdown(
                                        id="atm", options=OPTIONS["atm"], placeholder="Sélectionner"
                                    ),
                                ],
                                md=3,
                            ),
                            dbc.Col(
                                [
                                    html.Label("Saison"),
                                    dcc.Dropdown(
                                        id="saison",
                                        options=OPTIONS["saison"],
                                        placeholder="Sélectionner",
                                    ),
                                ],
                                md=3,
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Hr(),
                    # CONTEXTE
                    html.H5("Contexte de l'accident"),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label("Situation de l'accident"),
                                    dcc.Dropdown(
                                        id="situ",
                                        options=OPTIONS["situ"],
                                        placeholder="Sélectionner",
                                    ),
                                ],
                                md=3,
                            ),
                            dbc.Col(
                                [
                                    html.Label("Type de collision"),
                                    dcc.Dropdown(
                                        id="col", options=OPTIONS["col"], placeholder="Sélectionner"
                                    ),
                                ],
                                md=3,
                            ),
                        ],
                        className="mb-3",
                    ),
                    dbc.Button("🔮 Prédire", id="btn-predict", color="success", className="mt-3"),
                    html.H4(id="resultat", className="mt-4 text-center"),
                ]
            ),
        ]
    )
