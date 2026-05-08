"""
===============================================================================
PAGE EXPLORATION DES DONNÉES - VERSION FINALE
===============================================================================
KPI rectangulaires avec proportions + Graphiques avec labels textuels
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, norm
import sys
sys.path.append('..')
from utils import load_data, load_data_2, load_model

dash.register_page(__name__, path='/exploration', name='Exploration')

# Charger les données
df = load_data_2()
df_2 = load_data()

# ============================================================================
# LAYOUT
# ============================================================================

layout = dbc.Container([
    
    # En-tête
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2([
                    html.I(className="fas fa-chart-line me-3"),
                    "Exploration des Données"
                ], className="text-center text-orange mb-3"),
                html.P("Analyse interactive avec KPI, visualisations et tests statistiques", 
                      className="text-center lead"),
            ], className="card p-4")
        ], width=12)
    ], className="mb-4"),
    
    # ========================================================================
    # 12 KPI RECTANGULAIRES (6 par ligne) - PROPORTIONS
    # ========================================================================
    html.H4("Indicateurs Clés", className="text-orange mb-3 text-center"),
    
    # LIGNE 1 - 6 KPI
    dbc.Row([
        # KPI 1 - Total (seul en nombre absolu)
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-users fa-2x", style={'color': 'white'}),
                ], style={'position': 'absolute', 'left': '15px', 'top': '50%', 'transform': 'translateY(-50%)'}),
                html.Div([
                    html.H3(id='kpi-total-patients', className="mb-1", style={'fontSize': '1.8rem', 'fontWeight': 'bold'}),
                    html.P("Patients", className="mb-0", style={'fontSize': '0.85rem', 'opacity': '0.95'})
                ], style={'textAlign': 'center', 'marginLeft': '60px'})
            ], style={
                'background': 'linear-gradient(135deg, #FF6B35 0%, #F44336 100%)',
                'color': 'white',
                'padding': '1.2rem 1.5rem',
                'borderRadius': '12px',
                'position': 'relative',
                'boxShadow': '0 4px 12px rgba(255, 107, 53, 0.3)',
                'minHeight': '90px',
                'display': 'flex',
                'alignItems': 'center',
                'borderLeft': '5px solid rgba(255, 255, 255, 0.5)'
            })
        ], xs=12, md=2, className="mb-3"),
        
        # KPI 2 - Proportion Hommes
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-mars fa-2x", style={'color': 'white'}),
                ], style={'position': 'absolute', 'left': '15px', 'top': '50%', 'transform': 'translateY(-50%)'}),
                html.Div([
                    html.H3(id='kpi-hommes', className="mb-1", style={'fontSize': '1.8rem', 'fontWeight': 'bold'}),
                    html.P("Hommes", className="mb-0", style={'fontSize': '0.85rem', 'opacity': '0.95'})
                ], style={'textAlign': 'center', 'marginLeft': '60px'})
            ], style={
                'background': 'linear-gradient(135deg, #FF6B35 0%, #F44336 100%)',
                'color': 'white',
                'padding': '1.2rem 1.5rem',
                'borderRadius': '12px',
                'position': 'relative',
                'boxShadow': '0 4px 12px rgba(255, 107, 53, 0.3)',
                'minHeight': '90px',
                'display': 'flex',
                'alignItems': 'center',
                'borderLeft': '5px solid rgba(255, 255, 255, 0.5)'
            })
        ], xs=12, md=2, className="mb-3"),
        
        # KPI 3 - Proportion Femmes
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-venus fa-2x", style={'color': 'white'}),
                ], style={'position': 'absolute', 'left': '15px', 'top': '50%', 'transform': 'translateY(-50%)'}),
                html.Div([
                    html.H3(id='kpi-femmes', className="mb-1", style={'fontSize': '1.8rem', 'fontWeight': 'bold'}),
                    html.P("Femmes", className="mb-0", style={'fontSize': '0.85rem', 'opacity': '0.95'})
                ], style={'textAlign': 'center', 'marginLeft': '60px'})
            ], style={
                'background': 'linear-gradient(135deg, #FF6B35 0%, #F44336 100%)',
                'color': 'white',
                'padding': '1.2rem 1.5rem',
                'borderRadius': '12px',
                'position': 'relative',
                'boxShadow': '0 4px 12px rgba(255, 107, 53, 0.3)',
                'minHeight': '90px',
                'display': 'flex',
                'alignItems': 'center',
                'borderLeft': '5px solid rgba(255, 255, 255, 0.5)'
            })
        ], xs=12, md=2, className="mb-3"),
        
        # KPI 4 - Âge Moyen
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-birthday-cake fa-2x", style={'color': 'white'}),
                ], style={'position': 'absolute', 'left': '15px', 'top': '50%', 'transform': 'translateY(-50%)'}),
                html.Div([
                    html.H3(id='kpi-age-moyen', className="mb-1", style={'fontSize': '1.8rem', 'fontWeight': 'bold'}),
                    html.P("Âge Moyen", className="mb-0", style={'fontSize': '0.85rem', 'opacity': '0.95'})
                ], style={'textAlign': 'center', 'marginLeft': '60px'})
            ], style={
                'background': 'linear-gradient(135deg, #4CAF50 0%, #388E3C 100%)',
                'color': 'white',
                'padding': '1.2rem 1.5rem',
                'borderRadius': '12px',
                'position': 'relative',
                'boxShadow': '0 4px 12px rgba(76, 175, 80, 0.3)',
                'minHeight': '90px',
                'display': 'flex',
                'alignItems': 'center',
                'borderLeft': '5px solid rgba(255, 255, 255, 0.5)'
            })
        ], xs=12, md=2, className="mb-3"),
        
        # KPI 5 - Proportion Malades
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-heartbeat fa-2x", style={'color': 'white'}),
                ], style={'position': 'absolute', 'left': '15px', 'top': '50%', 'transform': 'translateY(-50%)'}),
                html.Div([
                    html.H3(id='kpi-malades', className="mb-1", style={'fontSize': '1.8rem', 'fontWeight': 'bold'}),
                    html.P("Malades", className="mb-0", style={'fontSize': '0.85rem', 'opacity': '0.95'})
                ], style={'textAlign': 'center', 'marginLeft': '60px'})
            ], style={
                'background': 'linear-gradient(135deg, #4CAF50 0%, #388E3C 100%)',
                'color': 'white',
                'padding': '1.2rem 1.5rem',
                'borderRadius': '12px',
                'position': 'relative',
                'boxShadow': '0 4px 12px rgba(76, 175, 80, 0.3)',
                'minHeight': '90px',
                'display': 'flex',
                'alignItems': 'center',
                'borderLeft': '5px solid rgba(255, 255, 255, 0.5)'
            })
        ], xs=12, md=2, className="mb-3"),
        
        # KPI 6 - Proportion Sains
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-shield-alt fa-2x", style={'color': 'white'}),
                ], style={'position': 'absolute', 'left': '15px', 'top': '50%', 'transform': 'translateY(-50%)'}),
                html.Div([
                    html.H3(id='kpi-sains', className="mb-1", style={'fontSize': '1.8rem', 'fontWeight': 'bold'}),
                    html.P("Sains", className="mb-0", style={'fontSize': '0.85rem', 'opacity': '0.95'})
                ], style={'textAlign': 'center', 'marginLeft': '60px'})
            ], style={
                'background': 'linear-gradient(135deg, #4CAF50 0%, #388E3C 100%)',
                'color': 'white',
                'padding': '1.2rem 1.5rem',
                'borderRadius': '12px',
                'position': 'relative',
                'boxShadow': '0 4px 12px rgba(76, 175, 80, 0.3)',
                'minHeight': '90px',
                'display': 'flex',
                'alignItems': 'center',
                'borderLeft': '5px solid rgba(255, 255, 255, 0.5)'
            })
        ], xs=12, md=2, className="mb-3"),
    ]),
    
    # LIGNE 2 - 6 KPI
    dbc.Row([
        # KPI 7 - BP Moyen
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-tachometer-alt fa-2x", style={'color': 'white'}),
                ], style={'position': 'absolute', 'left': '15px', 'top': '50%', 'transform': 'translateY(-50%)'}),
                html.Div([
                    html.H3(id='kpi-bp-moyen', className="mb-0", style={'fontSize': '1.8rem', 'fontWeight': 'bold'}),
                    html.P("BP Moyen", className="mb-0", style={'fontSize': '0.85rem', 'opacity': '0.9'})
                ], style={'textAlign': 'center', 'marginLeft': '60px'})
            ], style={
                'background': 'linear-gradient(135deg, #2196F3 0%, #1976D2 100%)',
                'color': 'white',
                'padding': '1.2rem 1.5rem',
                'borderRadius': '12px',
                'position': 'relative',
                'boxShadow': '0 4px 12px rgba(33, 150, 243, 0.3)',
                'minHeight': '90px',
                'display': 'flex',
                'alignItems': 'center',
                'borderLeft': '5px solid rgba(255, 255, 255, 0.5)'
            })
        ], xs=12, md=2, className="mb-3"),
        
        # KPI 8 - Cholestérol Moyen
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-heartbeat fa-2x", style={'color': 'white'}),
                ], style={'position': 'absolute', 'left': '15px', 'top': '50%', 'transform': 'translateY(-50%)'}),
                html.Div([
                    html.H3(id='kpi-cholesterol', className="mb-0", style={'fontSize': '1.8rem', 'fontWeight': 'bold'}),
                    html.P("Chol. Moy", className="mb-0", style={'fontSize': '0.85rem', 'opacity': '0.9'})
                ], style={'textAlign': 'center', 'marginLeft': '60px'})
            ], style={
                'background': 'linear-gradient(135deg, #2196F3 0%, #1976D2 100%)',
                'color': 'white',
                'padding': '1.2rem 1.5rem',
                'borderRadius': '12px',
                'position': 'relative',
                'boxShadow': '0 4px 12px rgba(33, 150, 243, 0.3)',
                'minHeight': '90px',
                'display': 'flex',
                'alignItems': 'center',
                'borderLeft': '5px solid rgba(255, 255, 255, 0.5)'
            })
        ], xs=12, md=2, className="mb-3"),
        
        # KPI 9 - Fréquence Max Moyenne
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-running fa-2x", style={'color': 'white'}),
                ], style={'position': 'absolute', 'left': '15px', 'top': '50%', 'transform': 'translateY(-50%)'}),
                html.Div([
                    html.H3(id='kpi-max-hr', className="mb-0", style={'fontSize': '1.8rem', 'fontWeight': 'bold'}),
                    html.P("Freq. Max", className="mb-0", style={'fontSize': '0.85rem', 'opacity': '0.9'})
                ], style={'textAlign': 'center', 'marginLeft': '60px'})
            ], style={
                'background': 'linear-gradient(135deg, #2196F3 0%, #1976D2 100%)',
                'color': 'white',
                'padding': '1.2rem 1.5rem',
                'borderRadius': '12px',
                'position': 'relative',
                'boxShadow': '0 4px 12px rgba(33, 150, 243, 0.3)',
                'minHeight': '90px',
                'display': 'flex',
                'alignItems': 'center',
                'borderLeft': '5px solid rgba(255, 255, 255, 0.5)'
            })
        ], xs=12, md=2, className="mb-3"),
        
        # KPI 10 - Proportion avec Diabète
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-chart-pie fa-2x", style={'color': 'white'}),
                ], style={'position': 'absolute', 'left': '15px', 'top': '50%', 'transform': 'translateY(-50%)'}),
                html.Div([
                    html.H3(id='kpi-diabetes', className="mb-0", style={'fontSize': '1.8rem', 'fontWeight': 'bold'}),
                    html.P("Diabète", className="mb-0", style={'fontSize': '0.85rem', 'opacity': '0.9'})
                ], style={'textAlign': 'center', 'marginLeft': '60px'})
            ], style={
                'background': 'linear-gradient(135deg, #9C27B0 0%, #7B1FA2 100%)',
                'color': 'white',
                'padding': '1.2rem 1.5rem',
                'borderRadius': '12px',
                'position': 'relative',
                'boxShadow': '0 4px 12px rgba(156, 39, 176, 0.3)',
                'minHeight': '90px',
                'display': 'flex',
                'alignItems': 'center',
                'borderLeft': '5px solid rgba(255, 255, 255, 0.5)'
            })
        ], xs=12, md=2, className="mb-3"),
        
        # KPI 11 - Proportion avec Angine
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-hand-holding-heart fa-2x", style={'color': 'white'}),
                ], style={'position': 'absolute', 'left': '15px', 'top': '50%', 'transform': 'translateY(-50%)'}),
                html.Div([
                    html.H3(id='kpi-angine', className="mb-0", style={'fontSize': '1.8rem', 'fontWeight': 'bold'}),
                    html.P("Angine", className="mb-0", style={'fontSize': '0.85rem', 'opacity': '0.9'})
                ], style={'textAlign': 'center', 'marginLeft': '60px'})
            ], style={
                'background': 'linear-gradient(135deg, #9C27B0 0%, #7B1FA2 100%)',
                'color': 'white',
                'padding': '1.2rem 1.5rem',
                'borderRadius': '12px',
                'position': 'relative',
                'boxShadow': '0 4px 12px rgba(156, 39, 176, 0.3)',
                'minHeight': '90px',
                'display': 'flex',
                'alignItems': 'center',
                'borderLeft': '5px solid rgba(255, 255, 255, 0.5)'
            })
        ], xs=12, md=2, className="mb-3"),
        
        # KPI 12 - Proportion BP Élevée (>140)
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-exclamation-triangle fa-2x", style={'color': 'white'}),
                ], style={'position': 'absolute', 'left': '15px', 'top': '50%', 'transform': 'translateY(-50%)'}),
                html.Div([
                    html.H3(id='kpi-bp-high', className="mb-0", style={'fontSize': '1.8rem', 'fontWeight': 'bold'}),
                    html.P("BP Élevée", className="mb-0", style={'fontSize': '0.85rem', 'opacity': '0.9'})
                ], style={'textAlign': 'center', 'marginLeft': '60px'})
            ], style={
                'background': 'linear-gradient(135deg, #9C27B0 0%, #7B1FA2 100%)',
                'color': 'white',
                'padding': '1.2rem 1.5rem',
                'borderRadius': '12px',
                'position': 'relative',
                'boxShadow': '0 4px 12px rgba(156, 39, 176, 0.3)',
                'minHeight': '90px',
                'display': 'flex',
                'alignItems': 'center',
                'borderLeft': '5px solid rgba(255, 255, 255, 0.5)'
            })
        ], xs=12, md=2, className="mb-3"),
    ], className="mb-5"),
    
    # ========================================================================
    # SECTION 1 : CIRCULAIRE + BARRE AVEC FILTRE
    # ========================================================================
    html.H4("Distribution des Variables", className="text-orange mb-3 text-center mt-4"),
    
    dbc.Row([
        # GAUCHE - Graphique Circulaire (Cible)
        dbc.Col([
            html.Div([
                html.H5("Répartition Cible", className="text-center mb-3"),
                dcc.Graph(id='pie-chart', config={'displayModeBar': False})
            ], className="card p-3", style={'height': '450px'})
        ], xs=12, md=6, className="mb-3"),
        
        # DROITE - Barre avec Filtre
        dbc.Col([
            html.Div([
                html.H5("Distribution par Variable", className="text-center mb-3"),
                dcc.Dropdown(
                    id='bar-variable-filter',
                    options=[
                        {'label': 'Sexe', 'value': 'sexe'},
                        {'label': 'Type de Douleur Thoracique', 'value': 'type_douleur_thoracique'},
                        {'label': 'ECG au Repos', 'value': 'électrocardiogramme_repos'},
                        {'label': 'Angine Induite', 'value': 'angine_induite_par_exercice'},
                        {'label': 'Pente ST', 'value': 'pente_st'},
                        {'label': 'Nombre de Vaisseaux', 'value': 'nombre_vaisseaux_majeurs'},
                        {'label': 'Thalassémie', 'value': 'thalassémie'},
                    ],
                    value='sexe',
                    clearable=False,
                    className="mb-3"
                ),
                dcc.Graph(id='bar-chart-filtered', config={'displayModeBar': False})
            ], className="card p-3", style={'height': '450px'})
        ], xs=12, md=6, className="mb-3"),
    ]),
    
    # ========================================================================
    # SECTION 2 : BOXPLOT + CIRCULAIRE QUALITATIVE
    # ========================================================================
    dbc.Row([
        # GAUCHE - Boxplot avec filtre
        dbc.Col([
            html.Div([
                html.H5("Boxplot par Cible", className="text-center mb-3"),
                dcc.Dropdown(
                    id='boxplot-variable-filter',
                    options=[
                        {'label': 'Âge', 'value': 'âge'},
                        {'label': 'Pression Artérielle', 'value': 'pression_artérielle_repos'},
                        {'label': 'Cholestérol', 'value': 'cholestérol'},
                        {'label': 'Fréquence Cardiaque Max', 'value': 'fréquence_cardiaque_maximale'},
                        {'label': 'Dépression ST', 'value': 'drépression_st'},
                    ],
                    value='âge',
                    clearable=False,
                    className="mb-3"
                ),
                dcc.Graph(id='boxplot-chart', config={'displayModeBar': False})
            ], className="card p-3", style={'height': '450px'})
        ], xs=12, md=6, className="mb-3"),
        
        # DROITE - Circulaire Qualitative avec filtre
        dbc.Col([
            html.Div([
                html.H5("Proportions Variable Qualitative", className="text-center mb-3"),
                dcc.Dropdown(
                    id='pie-qual-variable-filter',
                    options=[
                        {'label': 'Sexe', 'value': 'sexe'},
                        {'label': 'Type de Douleur Thoracique', 'value': 'type_douleur_thoracique'},
                        {'label': 'Diabète', 'value': 'glycémie_à_jeun'},
                        {'label': 'ECG au Repos', 'value': 'électrocardiogramme_repos'},
                        {'label': 'Angine Induite', 'value': 'angine_induite_par_exercice'},
                        {'label': 'Pente ST', 'value': 'pente_st'},
                        {'label': 'Nombre de Vaisseaux', 'value': 'nombre_vaisseaux_majeurs'},
                        {'label': 'Thalassémie', 'value': 'thalassémie'},
                    ],
                    value='sexe',
                    clearable=False,
                    className="mb-3"
                ),
                dcc.Graph(id='pie-qual-chart', config={'displayModeBar': False})
            ], className="card p-3", style={'height': '450px'})
        ], xs=12, md=6, className="mb-3"),
    ]),
    
    # ========================================================================
    # SECTION 3 : SCATTER + KHI-DEUX
    # ========================================================================
    html.H4("Analyses Avancées", className="text-orange mb-3 text-center mt-4"),
    
    dbc.Row([
        # GAUCHE - Nuage de points avec 2 filtres
        dbc.Col([
            html.Div([
                html.H5("Nuage de Points", className="text-center mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        html.Label("Variable X:", className="fw-bold"),
                        dcc.Dropdown(
                            id='scatter-x-filter',
                            options=[
                                {'label': 'Âge', 'value': 'âge'},
                                {'label': 'Pression Artérielle', 'value': 'pression_artérielle_repos'},
                                {'label': 'Cholestérol', 'value': 'cholestérol'},
                                {'label': 'Fréquence Cardiaque Max', 'value': 'fréquence_cardiaque_maximale'},
                                {'label': 'Dépression ST', 'value': 'dépression_st'},
                            ],
                            value='âge',
                            clearable=False
                        ),
                    ], xs=12, md=6, className="mb-2"),
                    
                    dbc.Col([
                        html.Label("Variable Y:", className="fw-bold"),
                        dcc.Dropdown(
                            id='scatter-y-filter',
                            options=[
                                {'label': 'Âge', 'value': 'âge'},
                                {'label': 'Pression Artérielle', 'value': 'pression_artérielle_repos'},
                                {'label': 'Cholestérol', 'value': 'cholestérol'},
                                {'label': 'Fréquence Cardiaque Max', 'value': 'fréquence_cardiaque_maximale'},
                                {'label': 'Dépression ST', 'value': 'dépression_st'},
                            ],
                            value='fréquence_cardiaque_maximale',
                            clearable=False
                        ),
                    ], xs=12, md=6, className="mb-2"),
                ]),
                
                dcc.Graph(id='scatter-plot', config={'displayModeBar': False})
            ], className="card p-3", style={'height': '500px'})
        ], xs=12, md=6, className="mb-3"),
        
        # DROITE - Test du Khi-deux (Heatmap)
        dbc.Col([
            html.Div([
                html.H5("Test du Khi-deux (Variables Qualitatives)", className="text-center mb-3"),
                html.P("Intensité des associations (p-values)", 
                      className="small text-center text-muted mb-3"),
                dcc.Graph(id='chi2-heatmap', config={'displayModeBar': False})
            ], className="card p-3", style={'height': '500px'})
        ], xs=12, md=6, className="mb-3"),
    ]),
    
    # ========================================================================
    # SECTION 4 : DISTRIBUTION + CORRÉLATION
    # ========================================================================
    html.H4("Distributions et Corrélations", className="text-orange mb-3 text-center mt-4"),
    
    dbc.Row([
        # Distribution globale avec loi normale
        dbc.Col([
            html.Div([
                html.H5("Distribution + Loi Normale", className="text-center mb-3"),
                dcc.Dropdown(
                    id='hist-variable-filter',
                    options=[
                        {'label': 'Âge', 'value': 'âge'},
                        {'label': 'Pression Artérielle', 'value': 'pression_artérielle_repos'},
                        {'label': 'Cholestérol', 'value': 'cholestérol'},
                        {'label': 'Fréquence Cardiaque Max', 'value': 'fréquence_cardiaque_maximale'},
                        {'label': 'Dépression ST', 'value': 'dépression_st'},
                    ],
                    value='âge',
                    clearable=False,
                    className="mb-3"
                ),
                dcc.Graph(id='histogram-normal', config={'displayModeBar': False})
            ], className="card p-3", style={'height': '500px'})
        ], xs=12, md=6, className="mb-3"),
        
        # Matrice de corrélation
        dbc.Col([
            html.Div([
                html.H5("Matrice de Corrélation", className="text-center mb-3"),
                dcc.Graph(id='correlation-matrix', config={'displayModeBar': False})
            ], className="card p-3", style={'height': '500px'})
        ], xs=12, md=6, className="mb-3"),
    ]),
    
], fluid=True, className="py-4")


# ============================================================================
# CALLBACKS
# ============================================================================

# Callback pour les 12 KPI (PROPORTIONS sauf Total)
@callback(
    [
        Output('kpi-total-patients', 'children'),
        Output('kpi-hommes', 'children'),
        Output('kpi-femmes', 'children'),
        Output('kpi-age-moyen', 'children'),
        Output('kpi-malades', 'children'),
        Output('kpi-sains', 'children'),
        Output('kpi-bp-moyen', 'children'),
        Output('kpi-cholesterol', 'children'),
        Output('kpi-max-hr', 'children'),
        Output('kpi-diabetes', 'children'),
        Output('kpi-angine', 'children'),
        Output('kpi-bp-high', 'children'),
    ],
    Input('pie-chart', 'id')
)
def update_kpis(_):
    """Calculer les 12 KPI avec proportions"""
    total = len(df)
    hommes_pct = round((len(df[df['sexe'] == 1]) / total) * 100, 1)
    femmes_pct = round((len(df[df['sexe'] == 0]) / total) * 100, 1)
    age_moyen = round(df['âge'].mean(), 1)
    malades_pct = round((len(df[df['maladie_cardiaque'] == 1]) / total) * 100, 1)
    sains_pct = round((len(df[df['maladie_cardiaque'] == 0]) / total) * 100, 1)
    bp_moyen = round(df['pression_artérielle_repos'].mean(), 0)
    chol_moyen = round(df['cholestérol'].mean(), 0)
    max_hr = round(df['fréquence_cardiaque_maximale'].mean(), 0)
    diabetes_pct = round((df['glycémie_à_jeun'].sum() / total) * 100, 1)
    angine_pct = round((df['angine_induite_par_exercice'].sum() / total) * 100, 1)
    bp_high_pct = round((len(df[df['pression_artérielle_repos'] > 140]) / total) * 100, 1)
    
    return (
        f"{total}", f"{hommes_pct}%", f"{femmes_pct}%", f"{age_moyen}",
        f"{malades_pct}%", f"{sains_pct}%", f"{int(bp_moyen)}", f"{int(chol_moyen)}",
        f"{int(max_hr)}", f"{diabetes_pct}%", f"{angine_pct}%", f"{bp_high_pct}%"
    )


# Callback pour le graphique circulaire (Cible avec labels textuels)
@callback(
    Output('pie-chart', 'figure'),
    Input('pie-chart', 'id')
)
def update_pie_chart(_):
    """Graphique circulaire de la cible avec labels"""
    counts = df['maladie_cardiaque'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=['Sain', 'Malade'],
        values=[counts[0], counts[1]],
        hole=0.4,
        marker=dict(colors=['#4CAF50', '#FF6B35']),
        textinfo='label+percent',
        textfont=dict(size=16, color='white', family='Arial Black'),
    )])
    
    fig.update_layout(
        showlegend=True,
        height=350,
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(font=dict(size=14))
    )
    
    return fig


# Callback pour le graphique en barre avec labels textuels
@callback(
    Output('bar-chart-filtered', 'figure'),
    Input('bar-variable-filter', 'value')
)
def update_bar_chart(variable):
    """Graphique en barre avec proportions (%) au lieu de totaux"""
    
    # Calculer les proportions
    crosstab = pd.crosstab(df_2[variable], df_2['maladie_cardiaque'].map({0: 'Sain', 1: 'Malade'}))
    crosstab_pct = crosstab.div(crosstab.sum(axis=1), axis=0) * 100
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Sain',
        x=crosstab_pct.index,
        y=crosstab_pct['Sain'] if 'Sain' in crosstab_pct.columns else [],
        marker_color='#4CAF50',
        text=[f'{v:.1f}%' for v in (crosstab_pct['Sain'] if 'Sain' in crosstab_pct.columns else [])],
        textposition='auto',
    ))
    
    fig.add_trace(go.Bar(
        name='Malade',
        x=crosstab_pct.index,
        y=crosstab_pct['Malade'] if 'Malade' in crosstab_pct.columns else [],
        marker_color='#FF6B35',
        text=[f'{v:.1f}%' for v in (crosstab_pct['Malade'] if 'Malade' in crosstab_pct.columns else [])],
        textposition='auto',
    ))
    
    fig.update_layout(
        barmode='group',
        height=300,
        margin=dict(t=20, b=80, l=40, r=20),
        xaxis_title="",
        yaxis_title="Proportion (%)",
        yaxis=dict(range=[0, 100]),
        xaxis=dict(tickangle=-45, tickfont=dict(size=11)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


# Callback pour le boxplot avec labels
@callback(
    Output('boxplot-chart', 'figure'),
    Input('boxplot-variable-filter', 'value')
)
def update_boxplot(variable):
    """Boxplot par cible avec labels textuels"""
    # BON - Utilise une copie locale
    df_local = df.copy()
    df_local['maladie_cardiaque'] = df_local['maladie_cardiaque'].map({0: 'Sain', 1: 'Malade'})
    
    fig = go.Figure()
    
    fig.add_trace(go.Box(
        y=df_local[df_local['maladie_cardiaque'] == 'Sain'][variable],
        name='Sain',
        marker_color='#4CAF50',
        boxmean='sd'
    ))
    
    fig.add_trace(go.Box(
        y=df_local[df_local['maladie_cardiaque'] == 'Malade'][variable],
        name='Malade',
        marker_color='#FF6B35',
        boxmean='sd'
    ))
    
    fig.update_layout(
        height=320,
        margin=dict(t=20, b=40, l=40, r=20),
        yaxis_title=variable.capitalize(),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


# Callback pour le circulaire qualitative
@callback(
    Output('pie-qual-chart', 'figure'),
    Input('pie-qual-variable-filter', 'value')
)
def update_pie_qual(variable):
    """Pie chart pour variable qualitative avec labels"""
    
    counts = df_2[variable].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=counts.index,
        values=counts.values,
        hole=0.4,
        textinfo='label+percent',
        textfont=dict(size=12, color='white'),
    )])
    
    fig.update_layout(
        height=350,
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    return fig


# Callback pour le scatter avec labels
@callback(
    Output('scatter-plot', 'figure'),
    [Input('scatter-x-filter', 'value'),
     Input('scatter-y-filter', 'value')]
)
def update_scatter(x_var, y_var):
    """Scatter avec labels textuels"""
    # BON - Utilise une copie locale
    #df_local = df.copy()
    #df_local['maladie_cardiaque'] = df_local['maladie_cardiaque'].map({0: 'Sain', 1: 'Malade'})
    
    fig = px.scatter(
        df, x=x_var, y=y_var, color='maladie_cardiaque',
        color_discrete_map={0: '#4CAF50', 1: '#FF6B35'},
        opacity=0.7
    )
    
    fig.update_layout(
        height=350,
        margin=dict(t=20, b=40, l=40, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(title="", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig


# Callback pour le Khi-deux
@callback(
    Output('chi2-heatmap', 'figure'),
    Input('chi2-heatmap', 'id')
)
def update_chi2_heatmap(_):
    """Heatmap des p-values du Khi-deux avec labels"""
    cat_vars = ['sexe', 'type_douleur_thoracique', 'glycémie_à_jeun', 'électrocardiogramme_repos', 'angine_induite_par_exercice', 'pente_st', 'nombre_vaisseaux_majeurs', 'thalassémie', 'maladie_cardiaque']
    var_labels = ['Sexe', 'Douleur', 'Diabète', 'ECG', 'Angine', 'Pente', 'Vaisseaux', 'Thal', 'Cible']
    
    n = len(cat_vars)
    p_values = np.zeros((n, n))
    
    for i, var1 in enumerate(cat_vars):
        for j, var2 in enumerate(cat_vars):
            if i == j:
                p_values[i, j] = 1.0
            else:
                try:
                    contingency = pd.crosstab(df_2[var1], df_2[var2])
                    # Vérifier que la table n'est pas vide
                    if contingency.size > 0 and contingency.sum().sum() > 0:
                        chi2, p_val, _, _ = chi2_contingency(contingency)
                        p_values[i, j] = p_val
                    else:
                        p_values[i, j] = 1.0  # Pas de relation si pas de données
                except (ValueError, ZeroDivisionError):
                    p_values[i, j] = 1.0  # En cas d'erreur, p-value = 1 (pas significatif)
    
    p_values_log = -np.log10(p_values + 1e-10)
    
    fig = go.Figure(data=go.Heatmap(
        z=p_values_log,
        x=var_labels,
        y=var_labels,
        colorscale='Reds',
        text=np.round(p_values, 4),
        texttemplate='%{text}',
        textfont={"size": 8},
        colorbar=dict(title="-log10(p)")
    ))
    
    fig.update_layout(
        height=380,
        margin=dict(t=20, b=60, l=60, r=20),
        xaxis=dict(tickangle=-45, tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


# Callback pour l'histogramme avec loi normale
@callback(
    Output('histogram-normal', 'figure'),
    Input('hist-variable-filter', 'value')
)
def update_histogram_normal(variable):
    """Histogramme global avec courbe normale"""
    data = df[variable].dropna()
    
    fig = go.Figure()
    
    # Histogramme
    fig.add_trace(go.Histogram(
        x=data,
        name='Distribution',
        marker_color='#2196F3',
        opacity=0.7,
        nbinsx=30
    ))
    
    # Courbe de la loi normale
    mu, std = data.mean(), data.std()
    x_range = np.linspace(data.min(), data.max(), 100)
    y_normal = norm.pdf(x_range, mu, std) * len(data) * (data.max() - data.min()) / 30
    
    fig.add_trace(go.Scatter(
        x=x_range,
        y=y_normal,
        name='Loi Normale',
        line=dict(color='#FF6B35', width=3)
    ))
    
    fig.update_layout(
        height=380,
        margin=dict(t=20, b=40, l=40, r=20),
        xaxis_title=variable.capitalize(),
        yaxis_title="Fréquence",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        bargap=0.1
    )
    
    return fig


# Callback pour la corrélation
@callback(
    Output('correlation-matrix', 'figure'),
    Input('correlation-matrix', 'id')
)
def update_correlation(_):
    """Matrice de corrélation"""
    num_vars = ['âge', 'pression_artérielle_repos', 'cholestérol', 'fréquence_cardiaque_maximale', 'dépression_st']
    var_labels = ['Âge', 'BP', 'Chol', 'Freq Max', 'Dép. ST']
    corr_matrix = df[num_vars].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=var_labels,
        y=var_labels,
        colorscale='RdBu',
        zmid=0,
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text}',
        textfont={"size": 14},
        colorbar=dict(title="Corr")
    ))
    
    fig.update_layout(
        height=380,
        margin=dict(t=20, b=60, l=60, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig
