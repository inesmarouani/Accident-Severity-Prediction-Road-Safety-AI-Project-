"""Callbacks pour la page de prédiction"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State
from src.services.api_client import api_client
from src.utils.validators import to_flag
from src.utils.constants import GRAVITE_LABELS, GRAVITE_COLORS


def register_prediction_callbacks(app):
    """Enregistre les callbacks de la page de prédiction"""
    
    @app.callback(
        Output("resultat", "children"),
        Input("btn-predict", "n_clicks"),
        State("is_passagers", "value"),
        State("localisation_pieton", "value"),
        State("age_cat", "value"),
        State("nb_proteges", "value"),
        State("trajet", "value"),
        State("situ", "value"),
        State("col", "value"),
        State("lum", "value"),
        State("agg", "value"),
        State("atm", "value"),
        State("saison", "value"),
        State("nb_usagers", "value"),
        State("nbv", "value"),
        State("vma", "value"),
        State("circ", "value"),
        prevent_initial_call=True
    )
    def predict(
        n_clicks,
        is_passagers,
        localisation_pieton,
        age_cat,
        nb_proteges,
        trajet,
        situ,
        col,
        lum,
        agg,
        atm,
        saison,
        nb_usagers,
        nbv,
        vma,
        circ
    ):
        """Callback pour la prédiction"""
        
        # Convertir les checklists
        is_passagers = to_flag(is_passagers)
        agg = 2 if to_flag(agg) == 1 else 1
        
        # Vérifier que tous les champs sont remplis
        required = [
            nb_proteges, nbv, vma, lum, saison, localisation_pieton,
            trajet, age_cat, is_passagers, circ, nb_usagers, atm, agg, col, situ
        ]
        
        if any(v is None for v in required):
            return dbc.Alert(
                "⚠️ Merci de remplir tous les champs.",
                color="warning"
            )
        
        # Préparer le payload
        payload = {
            "nb_proteges": nb_proteges,
            "nbv": nbv,
            "vma": vma,
            "lum": lum,
            "saison": saison,
            "localisation_pieton": localisation_pieton,
            "trajet": trajet,
            "age_cat": age_cat,
            "is_passagers": is_passagers,
            "circ": circ,
            "nb_usagers": nb_usagers,
            "atm": atm,
            "agg": agg,
            "col": col,
            "situ": situ
        }
        
        # Appeler l'API
        try:
            response = api_client.predict(payload)
            gravite = response["gravite_predite"]
            
            return dbc.Badge(
                GRAVITE_LABELS.get(gravite, gravite),
                color=GRAVITE_COLORS.get(gravite, "secondary"),
                className="p-3"
            )
            
        except Exception as e:
            return dbc.Alert(
                f"❌ Erreur API : {str(e)}",
                color="danger"
            )