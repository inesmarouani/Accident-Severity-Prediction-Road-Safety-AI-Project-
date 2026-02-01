import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import requests
import pandas as pd
import plotly.express as px

# ===========================
# Options des menus déroulants
# ===========================
OPTIONS = {
    "is_passagers": [
        {"label": "Non", "value": 0},
        {"label": "Oui", "value": 1}
    ],
    "col": [
        { "label": "1 – Deux véhicules - frontale ",           "value": 1 },
        { "label": "2 – Deux véhicules – par l’arrière",         "value": 2 },
        { "label": "3 – Deux véhicules – par le coté",         "value": 3 },
        { "label": "Trois véhicules et plus – en chaîn", "value": 4 },
        { "label": "Trois véhicules et plus - collisions multiples",      "value": 5 },
        { "label": " Autre collision",                    "value": 6 },
        { "label": " Sans collision",                    "value": 7 },
    ],
     
    "age_cat": [
        {"label": "0-2", "value": "0-2"},
        {"label": "3-11", "value": "3-11"},
        {"label": "12-17", "value": "12-17"},
        {"label": "18-64", "value": "18-64"},
        {"label": "65+", "value": "65+"},
    ],

    "trajet": [
        { "label": "Non renseigné",           "value": 0 },
        { "label": "Domicile – travail",       "value": 1 },
        { "label": "Domicile – école",         "value": 2 },
        { "label": "Courses – achats",         "value": 3 },
        { "label": "Utilisation professionnelle", "value": 4 },
        { "label": "Promenade – loisirs",      "value": 5 },
        { "label": "Autre",                    "value": 9 }
    ],
   
    "circ": [
        { "label": " A sens unique ",  "value": 1 },
        { "label": "Bidirectionnelle",  "value": 2 },
        { "label": "A chaussées séparées",  "value": 3 },
        { "label": "Avec voies d’affectation variable",  "value": 4 },
    ],

    
    "lum": [
    {"label": "Plein jour", "value": 1},
    {"label": "Crépuscule ou aube", "value": 2},
    {"label": "Nuit sans éclairage public", "value": 3},
    {"label": "Nuit avec éclairage public non allumé", "value": 4},
    {"label": "Nuit avec éclairage public allumé", "value": 5},
    ],

    "agg": [
        {"label": "Hors agglomération", "value": 1},
        {"label": "En agglomération", "value": 2}
    ],
    
    "atm": [
        {"label": "Normale", "value": 1},
        {"label": "Pluie légère ", "value": 2},
        {"label": "Pluie forte", "value": 3},
        {"label": "Neige - grêle", "value": 4},
        {"label": "Brouillard - fumé", "value": 5},
        {"label": "Vent fort - tempêt", "value": 6},
        {"label": "Temps éblouissant", "value": 7},
        {"label": "Temps couvert", "value": 8},
        {"label": "Autre", "value": 9},
    ],
    
    "situ": [
        {"label": " Aucun", "value": 0},
        {"label": "Sur chaussée", "value": 1},
        {"label": "Sur bande d’arrêt d’urgence ", "value": 2},
        {"label": "Sur accotement", "value": 3},
        {"label": "Sur trottoir", "value": 4},
        {"label": "Sur piste cyclable", "value": 5},
        {"label": " Sur autre voie spéciale", "value": 6},
        {"label": "Temps éblouissant", "value": 7},
        {"label": "Autres", "value": 8},
    ],

    "localisation_pieton": [
            {"label": " Sur chaussée", "value": 1},
            {"label": "Sur passage piéton", "value": 2},
            {"label": "Autre", "value": 3},
    ],

    "saison": [
        {"label": "été", "value": "ete"},
        {"label": "automne", "value": "automne"},
        {"label": "hiver", "value": "hiver"},
        {"label": "printemps", "value": "printemps"},
    ]
}

# =============================
# App Dash
# =============================
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
    pages_folder=""
)


# =============================
# Layout principal
# =============================
app.layout = dbc.Container([
    html.H2("🚦 Accidents routiers",
            className="text-center my-4"),

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


# =============================
# Router
# =============================
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def render_tab(tab):
    if tab == "tab-predict":
        return layout_prediction()
    elif tab == "tab-dashboard":
        return layout_dashboard()


# =============================
# Layout prédiction (complet)
# =============================
def layout_prediction():
    return dbc.Card([
        dbc.CardHeader("🔮 Prédiction de la gravité"),
        dbc.CardBody([

            # --- GENERAL ---
            html.H5("Informations générales"),
            dbc.Row([
                dbc.Col([
                    html.Label("Nb usagers"),
                    dbc.Input(id="nb_usagers", type="number", value=1, min=1, placeholder="Nb usagers")
                ], md=3),

                dbc.Col([
                    html.Label("Nb protégés"),
                    dbc.Input(id="nb_proteges", type="number", value=0, placeholder="Nb protégés")
                ], md=3),
            ], className="mb-3"),


            html.Hr(),

            # --- PROFIL ---
            html.H5("Profil des usagers"),
            dbc.Row([
                dbc.Col([
                    html.Label("Passager ?"),
                    dbc.Checklist(id="is_passagers", options=[{"label":"Oui","value":1}], value=[])
                ], md=3),

                dbc.Col([
                    html.Label("Catégorie d'âge"),
                    dcc.Dropdown(id="age_cat", options=OPTIONS["age_cat"], placeholder="age_cat")
                ], md=3),

                dbc.Col([
                    html.Label("Trajet"),
                    dcc.Dropdown(id="trajet", options=OPTIONS["trajet"], placeholder="trajet")
                ], md=3),
            ], className="mb-3"),

            html.Hr(),

            # --- CIRCULATION ---
            html.H5("Conditions de circulation"),
            dbc.Row([
                dbc.Col([
                    html.Label("agglomération?"),
                    dbc.Checklist(id="agg", options=[{"label":"Oui","value":1}], value=[])
                ], md=3),

                dbc.Col([
                    html.Label("Type de circulation"),
                    dcc.Dropdown(id="circ", options=OPTIONS["circ"], placeholder="circulation")
                ], md=3),

                dbc.Col([
                    html.Label("Vitesse maximale autorisée "),
                    dbc.Input(id="vma", type="number", value=50, min=10, step=10, placeholder="VMA")
                ], md=3),

                
                dbc.Col([
                     html.Label("Nombre de véhicules"),
                    dbc.Input(id="nbv", type="number", min=1, step=1, value=1)
                ], md=3),

                dbc.Col([
                    html.Label("Localisation des piétons"),
                    dcc.Dropdown(id="localisation_pieton", options=OPTIONS["localisation_pieton"], placeholder="localisation_pieton")
                ], md=3),
                
                dbc.Col([
                    html.Label("Luminosité"),
                    dcc.Dropdown(id="lum", options=OPTIONS["lum"], placeholder="lum")
                ], md=3),

                dbc.Col([
                    html.Label("Conditions atmosphériques"),
                    dcc.Dropdown(id="atm", options=OPTIONS["atm"], placeholder="atm")
                ], md=3),
                
                dbc.Col([
                    html.Label("Saison"),
                    dcc.Dropdown(id="saison", options=OPTIONS["saison"], placeholder="saison")
                ], md=3),
            ], className="mb-3"),

            # --- Contexte ---
            html.H5("Contexte de l'accident"),
            dbc.Row([

                dbc.Col([
                    html.Label("Situation de l’accident "),
                    dcc.Dropdown(id="situ", options=OPTIONS["situ"], placeholder="situ")
                ], md=3),

                dbc.Col([
                    html.Label("Type de collision :"),
                    dcc.Dropdown(id="col", options=OPTIONS["col"], placeholder="col")
                ], md=3),
            ], className="mb-3"),

            dbc.Alert("⚠️ Tous les champs doivent être remplis", color="warning",
                      id="alert", is_open=False),

            dbc.Button("🔮 Prédire", id="btn-predict",
                       color="success", className="mt-3"),

            html.H4(id="resultat", className="mt-4 text-center")
        ])
    ])


# =============================
# Callback prédiction (complet)
# =============================
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

    # Convert checklist values (list) to 0/1
    def to_flag(val):
        if isinstance(val, list):
            return 1 if 1 in val else 0
        if val in (1, "1", True):
            return 1
        return 0

    is_passagers = to_flag(is_passagers)
    agg = 2 if to_flag(agg) == 1 else 1


    required = [
        'nb_proteges', 'nbv', 'vma', 'lum', 'saison', 'localisation_pieton',
        'trajet', 'age_cat', 'is_passagers', 'circ', 'nb_usagers', 'atm', 'agg','col', 'situ'
    ]

    if any(v is None for v in required):
        return dbc.Alert("⚠️ Merci de remplir tous les champs.", color="warning")

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


    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=payload,
            timeout=10
        )

        if response.status_code == 422:
            return dbc.Alert(
                "⚠️ Merci de compléter tous les champs (ou vérifier les valeurs).",
                color="warning"
            )

        response.raise_for_status()
        gravite = response.json()["gravite_predite"]

    except Exception as e:
        return dbc.Alert(f"❌ Erreur API : {e}", color="danger")


    labels = {
    0: "🟢 Accident sans blessé grave",
    1: "🔴 Accident avec blessés graves/mortel",
    }

    colors = {
        0: "success",   # vert
        1: "warning"    # orange
    }

    return dbc.Badge(
        labels.get(gravite, gravite),
        color=colors.get(gravite, "secondary"),
        className="p-3"
    )



# =============================
# Dashboard
# =============================
df = pd.read_csv("../data/accidents_clean.csv")

# renommer la colonne
df.rename(columns={"grav_accident": "gravite"}, inplace=True)

def layout_dashboard():
    return dbc.Container([

        # FILTRES
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id="filter_dep",
                options=[{"label": d, "value": d} for d in sorted(df["dep"].unique())],
                placeholder="Département",
                multi=True
            ), md=4),

            dbc.Col(dcc.Dropdown(
                id="filter_saison",
                options=[{"label": s, "value": s} for s in sorted(df["saison"].unique())],
                placeholder="Saison",
                multi=True
            ), md=4),

            dbc.Col(dcc.Dropdown(
                id="filter_gravite",
                options=[
                    {"label": "Sans blessé", "value": 0},
                    {"label": "Avec blessés", "value": 1},
                    {"label": "Mortel", "value": 2},
                ],
                placeholder="Gravité",
                multi=True
            ), md=4),
        ], className="mb-4"),

        # KPI
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Total accidents"),
                dbc.CardBody(html.H3(id="kpi_total"))
            ]), md=3),

            dbc.Col(dbc.Card([
                dbc.CardHeader("% mortels"),
                dbc.CardBody(html.H3(id="kpi_mortels"))
            ]), md=3),

            dbc.Col(dbc.Card([
                dbc.CardHeader("% avec blessés"),
                dbc.CardBody(html.H3(id="kpi_blesses"))
            ]), md=3),

            dbc.Col(dbc.Card([
                dbc.CardHeader("% weekend"),
                dbc.CardBody(html.H3(id="kpi_weekend"))
            ]), md=3),
        ], className="mb-4"),

        # GRAPHIQUES
        dbc.Row([
            dbc.Col(dcc.Graph(id="graph_gravite"), md=6),
            dbc.Col(dcc.Graph(id="graph_saison"), md=6),
        ]),

        dbc.Row([
            dbc.Col(dcc.Graph(id="graph_dep"), md=6),
            dbc.Col(dcc.Graph(id="graph_lum"), md=6),
        ]),

        dbc.Row([
            dbc.Col(dcc.Graph(id="graph_atm"), md=6),
            dbc.Col(dcc.Graph(id="graph_nbveh"), md=6),
        ]),
    ], fluid=True)
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
    ]
)
def update_dashboard(dep, saison, gravite):

    # Filtrer le dataframe
    dff = df.copy()
    if dep:
        dff = dff[dff["dep"].isin(dep)]
    if saison:
        dff = dff[dff["saison"].isin(saison)]
    if gravite:
        dff = dff[dff["gravite"].isin(gravite)]

    # KPIs
    total = len(dff)
    mortels = round((dff["gravite"] == 2).mean() * 100, 1) if total else 0
    blesses = round((dff["gravite"] == 1).mean() * 100, 1) if total else 0
    weekend = round((dff["is_weekend"] == 1).mean() * 100, 1) if total else 0

    # Graphiques
    fig_gravite = px.histogram(dff, x="gravite", color="gravite",
                               title="Distribution de la gravité")

    fig_saison = px.histogram(dff, x="saison", color="gravite",
                              title="Gravité par saison")

    fig_dep = px.histogram(dff, x="dep", color="gravite",
                           title="Gravité par département")

    fig_lum = px.histogram(dff, x="lum", color="gravite",
                           title="Gravité par luminosité")

    fig_atm = px.histogram(dff, x="atm", color="gravite",
                           title="Gravité par météo")

    fig_nbveh = px.scatter(dff, x="nb_vehicules", y="nb_usagers",
                           color="gravite",
                           title="Nb véhicules vs nb usagers (gravité)")

    return total, f"{mortels}%", f"{blesses}%", f"{weekend}%", \
           fig_gravite, fig_saison, fig_dep, fig_lum, fig_atm, fig_nbveh


if __name__ == "__main__":
    app.run(debug=True)

