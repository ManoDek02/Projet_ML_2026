
"""
===============================================================================
PAGE DE GARDE - LANDING PAGE
===============================================================================
Page d'accueil avec images défilantes et bouton d'entrée
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', name='Landing')

# ============================================================================
# IMAGES DE SANTÉ (URLs en ligne)
# ============================================================================

health_images = [
    "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=1920&h=1080&fit=crop",  # Médecin avec stéthoscope
    "https://images.unsplash.com/photo-1559757175-5700dde675bc?w=1920&h=1080&fit=crop",  # Cardiogramme
    "https://images.unsplash.com/photo-1631217868264-e5b90bb7e133?w=1920&h=1080&fit=crop",  # Cœur médical
    "https://images.unsplash.com/photo-1579154204601-01588f351e67?w=1920&h=1080&fit=crop",  # Technologie médicale
    "https://images.unsplash.com/photo-1551076805-e1869033e561?w=1920&h=1080&fit=crop",  # Hôpital moderne
]

# ============================================================================
# LAYOUT
# ============================================================================

layout = html.Div([
    
    # Carrousel d'images en arrière-plan
    dcc.Interval(id='image-interval', interval=3000, n_intervals=0),
    
    html.Div([
        html.Div(id='background-carousel', style={
            'position': 'fixed',
            'top': 0,
            'left': 0,
            'width': '100%',
            'height': '100%',
            'zIndex': -1,
            'backgroundSize': 'cover',
            'backgroundPosition': 'center',
            'backgroundRepeat': 'no-repeat',
            'transition': 'background-image 1s ease-in-out',
        })
    ]),
    
    # Overlay sombre
    html.Div(style={
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'width': '100%',
        'height': '100%',
        'backgroundColor': 'rgba(0, 0, 0, 0.6)',
        'zIndex': 0,
    }),
    
    # Contenu principal
    html.Div([
        dbc.Container([
            
            # Titre principal
            html.Div([
                html.H1([
                    html.I(className="fas fa-heartbeat me-3", style={'color': '#FF6B35'}),
                    "CardioPredict ML"
                ], className="text-center text-white mb-3", 
                   style={'fontSize': '4.5rem', 'fontWeight': 'bold', 
                         'textShadow': '3px 3px 6px rgba(0,0,0,0.8)',
                         'animation': 'fadeInDown 1s'}),
                
                html.H3("Intelligence Artificielle pour la Prédiction des Maladies Cardiaques",
                       className="text-center text-white mb-5",
                       style={'fontSize': '1.8rem', 'fontWeight': '300',
                             'textShadow': '2px 2px 4px rgba(0,0,0,0.8)',
                             'animation': 'fadeInUp 1.5s'}),
            ], className="mb-5"),
            
            # Bouton d'entrée
            html.Div([
                dbc.Button([
                    html.I(className="fas fa-arrow-right me-2"),
                    "DÉCOUVRIR LE PROJET"
                ], href="/accueil", size="lg", 
                   style={
                       'background': 'linear-gradient(135deg, #FF6B35 0%, #F44336 100%)',
                       'border': 'none',
                       'padding': '1rem 3rem',
                       'fontSize': '1.3rem',
                       'fontWeight': 'bold',
                       'borderRadius': '50px',
                       'boxShadow': '0 8px 20px rgba(255, 107, 53, 0.4)',
                       'transition': 'all 0.3s',
                       'animation': 'pulse 2s infinite'
                   })
            ], className="text-center mb-5"),
            
            # Info rapide
            html.Div([
                html.P([
                    html.I(className="fas fa-database me-2"),
                    "297 patients analysés",
                    html.Span(" | ", className="mx-3"),
                    html.I(className="fas fa-chart-pie me-2"),
                    "6 algorithmes ML",
                    html.Span(" | ", className="mx-3"),
                    html.I(className="fas fa-award me-2"),
                    "85%+ de précision"
                ], className="text-center text-white",
                   style={'fontSize': '1.2rem', 'opacity': '0.9',
                         'textShadow': '1px 1px 3px rgba(0,0,0,0.8)'})
            ], style={'animation': 'fadeIn 3s'})
            
        ], style={'paddingTop': '10vh'})
    ], style={
        'position': 'relative',
        'zIndex': 1,
        'minHeight': '100vh',
        'display': 'flex',
        'alignItems': 'center'
    }),
    
], style={'overflow': 'hidden'})


# ============================================================================
# CALLBACK - Changer l'image de fond toutes les 3 secondes
# ============================================================================

@callback(
    Output('background-carousel', 'style'),
    Input('image-interval', 'n_intervals')
)
def update_background(n):
    """Faire défiler les images de fond"""
    current_image = health_images[n % len(health_images)]
    
    return {
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'width': '100%',
        'height': '100%',
        'zIndex': -1,
        'backgroundImage': f'url({current_image})',
        'backgroundSize': 'cover',
        'backgroundPosition': 'center',
        'backgroundRepeat': 'no-repeat',
        'transition': 'background-image 1s ease-in-out',
    }