
"""
===============================================================================
APP.PY - Application Dash Principale
===============================================================================
"""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import os

# Initialiser l'app Dash
app = dash.Dash(
    __name__,
    use_pages=True,
    pages_folder='pages',
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
    ],
    suppress_callback_exceptions=True,
    title="CardioPredict ML"
)

server = app.server

# ============================================================================
# NAVBAR MODERNE
# ============================================================================

navbar = html.Div([
    # Section supérieure - Logo et nom sur fond blanc (TOUTE LA LARGEUR)
    html.Div([
        html.A([
            html.Img(src="/assets/logo.png", className="navbar-logo"),
            html.Span([
                html.I(className="fas fa-heartbeat me-2"),
                "FAPE"
            ])
        ], href="/accueil", className="navbar-brand-custom")
    ], className="navbar-top"),
    
    # Bande orange en bas avec les liens (TOUTE LA LARGEUR)
    html.Div([
        html.Ul([
            html.Li([
                dcc.Link([
                    html.I(className="fas fa-home me-2"),
                    "Accueil"
                ], href="/accueil", className="navbar-link-custom", id="link-accueil")
            ]),
            html.Li([
                dcc.Link([
                    html.I(className="fas fa-chart-line me-2"),
                    "Exploration"
                ], href="/exploration", className="navbar-link-custom", id="link-exploration")
            ]),
            html.Li([
                dcc.Link([
                    html.I(className="fas fa-brain me-2"),
                    "Modélisation"
                ], href="/modelisation", className="navbar-link-custom", id="link-modelisation")
            ]),
            html.Li([
                dcc.Link([
                    html.I(className="fas fa-user-md me-2"),
                    "Prédiction"
                ], href="/prediction", className="navbar-link-custom", id="link-prediction")
            ]),
            html.Li([
                dcc.Link([
                    html.I(className="fas fa-history me-2"),
                    "Historique"
                ], href="/history", className="navbar-link-custom", id="link-history")
            ]),
        ], className="navbar-links")
    ], className="navbar-bottom")
], className="custom-navbar", style={'position': 'sticky', 'top': 0, 'zIndex': 1000, 'marginBottom': '2rem'})

# ============================================================================
# LAYOUT PRINCIPAL
# ============================================================================

app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    
    # Navbar (caché sur landing page)
    html.Div(navbar, id='navbar-container'),
    
    # Contenu des pages
    dash.page_container,
    
    # Footer (caché sur landing page)
    html.Div([
        html.Hr(className="mt-5"),
        html.Footer([
            html.P([
                html.I(className="fas fa-graduation-cap me-2"),
                "Projet ML - Classification Maladies Cardiaques"
            ], className="text-center text-muted mb-2"),
            html.P([
                html.Strong("Équipe: "),
                "Fatoumata BAH, Poko Ibrahima NOBA, Emmanuel DOSSEKOU, Armand DJEKONBE"
            ], className="text-center text-muted small mb-2"),
            html.P([
                html.I(className="fas fa-chalkboard-teacher me-2"),
                "Superviseur: Mme Fatou SALL"
            ], className="text-center text-muted small")
        ], className="mb-4")
    ], id='footer-container')
], fluid=True)

# ============================================================================
# CALLBACK POUR CACHER NAVBAR/FOOTER SUR LANDING PAGE
# ============================================================================

@callback(
    [
        Output('navbar-container', 'style'),
        Output('footer-container', 'style'),
    ],
    Input('url', 'pathname')
)
def toggle_navbar_footer(pathname):
    """Cacher navbar et footer sur la page landing"""
    if pathname == '/' or pathname is None:
        # Page landing - cacher navbar et footer
        return {'display': 'none'}, {'display': 'none'}
    else:
        # Autres pages - afficher navbar et footer
        return {'display': 'block'}, {'display': 'block'}

# ============================================================================
# CALLBACK POUR ACTIVER LE LIEN ACTIF
# ============================================================================

@callback(
    [
        Output('link-accueil', 'className'),
        Output('link-exploration', 'className'),
        Output('link-modelisation', 'className'),
        Output('link-prediction', 'className'),
    ],
    Input('url', 'pathname')
)
def update_active_link(pathname):
    """Mettre en surbrillance le lien actif"""
    base_class = "navbar-link-custom"
    active_class = "navbar-link-custom navbar-link-active"
    
    # Déterminer quelle page est active
    if pathname == '/accueil' or pathname == '/':
        return active_class, base_class, base_class, base_class
    elif pathname == '/exploration':
        return base_class, active_class, base_class, base_class
    elif pathname == '/modelisation':
        return base_class, base_class, active_class, base_class
    elif pathname == '/prediction':
        return base_class, base_class, base_class, active_class
    else:
        return base_class, base_class, base_class, base_class

# ============================================================================
# LANCEMENT
# ============================================================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(host='0.0.0.0', port=port, debug=False)
