"""Point d'entrée principal de l'application Dash"""

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

from src.config import config
from src.layouts.dashboard import create_dashboard_layout
from src.layouts.prediction import create_prediction_layout
from src.callbacks.dashboard import register_dashboard_callbacks
from src.callbacks.prediction import register_prediction_callbacks


# Initialiser l'application Dash
app = dash.Dash(
    __name__,
    external_stylesheets=[getattr(dbc.themes, config.THEME)],
    suppress_callback_exceptions=True
)

# Layout principal avec navigation par onglets
app.layout = dbc.Container([
    html.H2(
        "🚦 Accidents routiers",
        className="text-center my-4"
    ),
    
    dcc.Tabs(
        id="tabs",
        value="tab-dashboard",
        children=[
            dcc.Tab(label="📊 Dashboard", value="tab-dashboard"),
            dcc.Tab(label="🔮 Prédiction", value="tab-predict"),
        ]
    ),
    
    html.Div(id="tab-content", className="mt-4")
], fluid=True)


# Callback pour le routing entre les onglets
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def render_tab(tab):
    """Affiche le contenu de l'onglet sélectionné"""
    if tab == "tab-predict":
        return create_prediction_layout()
    elif tab == "tab-dashboard":
        return create_dashboard_layout()


# Enregistrer les callbacks
register_dashboard_callbacks(app)
register_prediction_callbacks(app)


# Point d'entrée
if __name__ == "__main__":
    app.run(
        host=config.APP_HOST,
        port=config.APP_PORT,
        debug=config.DEBUG
    )