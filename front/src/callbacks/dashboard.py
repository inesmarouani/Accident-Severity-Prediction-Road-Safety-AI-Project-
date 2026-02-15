"""Callbacks pour le dashboard"""

import plotly.express as px
from dash import Input, Output

from src.services.data_loader import data_loader


def register_dashboard_callbacks(app):
    """Enregistre les callbacks du dashboard"""

    @app.callback(
        [
            Output("kpi_total", "children"),
            Output("kpi_mortels", "children"),
            Output("kpi_blesses", "children"),
            Output("kpi_weekend", "children"),
            Output("graph_gravite", "figure"),
            Output("graph_saison", "figure"),
            Output("graph_dep", "figure"),
            Output("graph_lum", "figure"),
            Output("graph_atm", "figure"),
            Output("graph_nbveh", "figure"),
        ],
        [
            Input("filter_dep", "value"),
            Input("filter_saison", "value"),
            Input("filter_gravite", "value"),
        ],
    )
    def update_dashboard(dep, saison, gravite):
        """Met à jour le dashboard selon les filtres"""

        # Filtrer les données
        dff = data_loader.filter_data(dep=dep, saison=saison, gravite=gravite)

        # Calculer les KPIs
        total = len(dff)
        mortels = round((dff["gravite"] == 2).mean() * 100, 1) if total else 0
        blesses = round((dff["gravite"] == 1).mean() * 100, 1) if total else 0
        weekend = round((dff["is_weekend"] == 1).mean() * 100, 1) if total else 0

        # Créer les graphiques
        fig_gravite = px.histogram(
            dff, x="gravite", color="gravite", title="Distribution de la gravité"
        )

        fig_saison = px.histogram(dff, x="saison", color="gravite", title="Gravité par saison")

        fig_dep = px.histogram(dff, x="dep", color="gravite", title="Gravité par département")

        fig_lum = px.histogram(dff, x="lum", color="gravite", title="Gravité par luminosité")

        fig_atm = px.histogram(dff, x="atm", color="gravite", title="Gravité par météo")

        fig_nbveh = px.scatter(
            dff,
            x="nb_vehicules",
            y="nb_usagers",
            color="gravite",
            title="Nb véhicules vs nb usagers (gravité)",
        )

        return (
            total,
            f"{mortels}%",
            f"{blesses}%",
            f"{weekend}%",
            fig_gravite,
            fig_saison,
            fig_dep,
            fig_lum,
            fig_atm,
            fig_nbveh,
        )
