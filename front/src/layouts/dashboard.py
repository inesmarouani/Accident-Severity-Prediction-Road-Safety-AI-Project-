"""Layout de la page dashboard"""

import dash_bootstrap_components as dbc
from dash import dcc, html

from src.services.data_loader import data_loader

# Charger les données pour les options
df = data_loader.get_dataframe()


def create_dashboard_layout():
    """Crée le layout du dashboard"""

    return dbc.Container(
        [
            # FILTRES
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Dropdown(
                            id="filter_dep",
                            options=[{"label": d, "value": d} for d in sorted(df["dep"].unique())],
                            placeholder="Département",
                            multi=True,
                        ),
                        md=4,
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="filter_saison",
                            options=[
                                {"label": s, "value": s} for s in sorted(df["saison"].unique())
                            ],
                            placeholder="Saison",
                            multi=True,
                        ),
                        md=4,
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="filter_gravite",
                            options=[
                                {"label": "Sans blessé", "value": 0},
                                {"label": "Avec blessés", "value": 1},
                                {"label": "Mortel", "value": 2},
                            ],
                            placeholder="Gravité",
                            multi=True,
                        ),
                        md=4,
                    ),
                ],
                className="mb-4",
            ),
            # KPI
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Total accidents"),
                                dbc.CardBody(html.H3(id="kpi_total")),
                            ]
                        ),
                        md=3,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [dbc.CardHeader("% mortels"), dbc.CardBody(html.H3(id="kpi_mortels"))]
                        ),
                        md=3,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("% avec blessés"),
                                dbc.CardBody(html.H3(id="kpi_blesses")),
                            ]
                        ),
                        md=3,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [dbc.CardHeader("% weekend"), dbc.CardBody(html.H3(id="kpi_weekend"))]
                        ),
                        md=3,
                    ),
                ],
                className="mb-4",
            ),
            # GRAPHIQUES
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="graph_gravite"), md=6),
                    dbc.Col(dcc.Graph(id="graph_saison"), md=6),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="graph_dep"), md=6),
                    dbc.Col(dcc.Graph(id="graph_lum"), md=6),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="graph_atm"), md=6),
                    dbc.Col(dcc.Graph(id="graph_nbveh"), md=6),
                ]
            ),
        ],
        fluid=True,
    )
