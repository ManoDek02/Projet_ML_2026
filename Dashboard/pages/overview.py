
"""
===============================================================================
PAGE ACCUEIL - PRÉSENTATION DU PROJET
===============================================================================
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/accueil', name='Accueil')

# ============================================================================
# LAYOUT
# ============================================================================

layout = dbc.Container([
    
    # ========================================================================
    # EN-TÊTE
    # ========================================================================
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1([
                    html.I(className="fas fa-heartbeat me-3", style={'color': '#FF6B35'}),
                    "CardioPredict ML"
                ], className="text-center mb-3", style={'color': '#FF6B35', 'fontWeight': 'bold'}),
                html.H4("Intelligence Artificielle pour la Prédiction des Maladies Cardiaques",
                       className="text-center text-muted mb-4")
            ])
        ], width=12)
    ], className="mb-5"),
    
    # ========================================================================
    # CONTEXTE ET PROBLÉMATIQUE
    # ========================================================================
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3([
                    html.I(className="fas fa-book-medical me-2"),
                    "Contexte & Problématique"
                ], className="text-orange mb-3 text-center"),
                
                html.P([
                    "Les maladies cardiovasculaires sont la ",
                    html.Strong("première cause de mortalité dans le monde", style={'color': '#FF6B35'}),
                    ", avec plus de 17,9 millions de décès par an selon l'",
                    html.A("OMS (2023)", 
                          href="https://www.who.int/fr/news-room/fact-sheets/detail/cardiovascular-diseases-(cvds)",
                          target="_blank",
                          style={'color': '#2196F3', 'textDecoration': 'underline', 'fontWeight': 'bold'}),
                    ". Un diagnostic précoce et précis peut sauver des vies et réduire les coûts de santé."
                ], className="lead mb-3"),
                
                html.P([
                    "Cependant, le diagnostic traditionnel repose sur l'expertise médicale et des examens coûteux, "
                    "ce qui limite l'accessibilité dans certaines régions. ",
                    html.Strong("Notre solution utilise le Machine Learning", style={'color': '#4CAF50'}),
                    " pour prédire les risques cardiovasculaires à partir de données cliniques simples."
                ], className="mb-0")
                
            ], className="card p-4")
        ], width=12, className="mb-4")
    ]),
    
    # ========================================================================
    # OBJECTIFS
    # ========================================================================
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3([
                    html.I(className="fas fa-bullseye me-2"),
                    "Objectifs du Projet"
                ], className="text-orange mb-4 text-center"),
                
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-check-circle fa-2x mb-3", style={'color': '#4CAF50'}),
                                html.H5("Prédiction Précise", className="mb-2"),
                                html.P("Développer un modèle ML capable de prédire la présence de maladies cardiaques avec une précision supérieure à 85%.",
                                      className="small text-muted")
                            ], className="text-center p-3")
                        ], style={'background': '#F5F5F5', 'borderRadius': '12px', 'height': '100%'})
                    ], xs=12, md=4, className="mb-3"),
                    
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-chart-line fa-2x mb-3", style={'color': '#2196F3'}),
                                html.H5("Analyse Exploratoire", className="mb-2"),
                                html.P("Explorer et visualiser les données pour identifier les facteurs de risque clés et leurs corrélations.",
                                      className="small text-muted")
                            ], className="text-center p-3")
                        ], style={'background': '#F5F5F5', 'borderRadius': '12px', 'height': '100%'})
                    ], xs=12, md=4, className="mb-3"),
                    
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-user-md fa-2x mb-3", style={'color': '#FF6B35'}),
                                html.H5("Aide à la Décision", className="mb-2"),
                                html.P("Fournir un outil interactif permettant aux professionnels de santé d'évaluer rapidement les risques cardiaques.",
                                      className="small text-muted")
                            ], className="text-center p-3")
                        ], style={'background': '#F5F5F5', 'borderRadius': '12px', 'height': '100%'})
                    ], xs=12, md=4, className="mb-3"),
                ])
                
            ], className="card p-4")
        ], width=12, className="mb-4")
    ]),
    
    # ========================================================================
    # DONNÉES UTILISÉES
    # ========================================================================
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3([
                    html.I(className="fas fa-database me-2"),
                    "Données Utilisées"
                ], className="text-orange mb-4 text-center"),
                
                dbc.Row([
                    # Colonne gauche - Source & Description
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.H5([
                                    html.I(className="fas fa-info-circle me-2", style={'color': '#FF6B35'}),
                                    "Source & Description"
                                ], className="mb-3 text-center"),
                                
                                html.Div([
                                    html.Div([
                                        html.I(className="fas fa-database me-2", style={'color': '#4CAF50'}),
                                        html.Strong("Source: "),
                                        "UCI Heart Disease Dataset"
                                    ], className="mb-2 p-2", 
                                       style={'background': 'white', 'borderRadius': '8px', 'border': '2px solid #E0E0E0'}),
                                    
                                    html.Div([
                                        html.I(className="fas fa-users me-2", style={'color': '#2196F3'}),
                                        html.Strong("Taille: "),
                                        "297 patients (après nettoyage)"
                                    ], className="mb-2 p-2", 
                                       style={'background': 'white', 'borderRadius': '8px', 'border': '2px solid #E0E0E0'}),
                                    
                                    html.Div([
                                        html.I(className="fas fa-columns me-2", style={'color': '#FFC107'}),
                                        html.Strong("Features: "),
                                        "13 variables cliniques"
                                    ], className="mb-2 p-2", 
                                       style={'background': 'white', 'borderRadius': '8px', 'border': '2px solid #E0E0E0'}),
                                    
                                    html.Div([
                                        html.I(className="fas fa-crosshairs me-2", style={'color': '#E91E63'}),
                                        html.Strong("Cible: "),
                                        "Présence (1) ou absence (0)"
                                    ], className="mb-2 p-2", 
                                       style={'background': 'white', 'borderRadius': '8px', 'border': '2px solid #E0E0E0'}),
                                    
                                    html.Div([
                                        html.I(className="fas fa-calendar-alt me-2", style={'color': '#9C27B0'}),
                                        html.Strong("Période: "),
                                        "1988 - 2020"
                                    ], className="mb-3 p-2", 
                                       style={'background': 'white', 'borderRadius': '8px', 'border': '2px solid #E0E0E0'}),
                                ]),
                                
                                html.Div([
                                    dbc.Button([
                                        html.I(className="fas fa-download me-2"),
                                        "Accéder aux Données"
                                    ], href="https://archive.ics.uci.edu/dataset/45/heart+disease", 
                                       target="_blank", color="primary", className="w-100")
                                ])
                                
                            ], className="p-3")
                        ], style={'background': '#FFF8F3', 'borderRadius': '12px', 
                                'border': '3px solid #FFD4B8', 'height': '100%'})
                    ], xs=12, md=6, className="mb-3"),
                    
                    # Colonne droite - Variables (RÉORGANISÉ - ALIGNEMENT GAUCHE)
                    dbc.Col([
                        html.Div([
                            html.H5([
                                html.I(className="fas fa-list-ul me-2", style={'color': '#FF6B35'}),
                                "Variables Principales"
                            ], className="mb-3 text-center"),
                            
                            # LIGNE 1: Imagerie + Démographiques
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        html.Div([
                                            html.I(className="fas fa-x-ray me-2", style={'color': '#9C27B0'}),
                                            html.Strong("Imagerie")
                                        ], className="mb-2"),
                                        html.P("Vaisseaux colorés, Thalassémie", className="small text-muted mb-0")
                                    ], className="p-3", 
                                       style={'background': 'white', 'borderRadius': '10px', 
                                             'border': '2px solid #9C27B0', 'borderLeft': '5px solid #9C27B0'})
                                ], xs=12, md=6, className="mb-2"),
                                
                                dbc.Col([
                                    html.Div([
                                        html.Div([
                                            html.I(className="fas fa-user me-2", style={'color': '#2196F3'}),
                                            html.Strong("Démographiques")
                                        ], className="mb-2"),
                                        html.P("Âge, Sexe", className="small text-muted mb-0")
                                    ], className="p-3", 
                                       style={'background': 'white', 'borderRadius': '10px', 
                                             'border': '2px solid #2196F3', 'borderLeft': '5px solid #2196F3'})
                                ], xs=12, md=6, className="mb-2"),
                            ]),
                            
                            # LIGNE 2: Cliniques + Cardiologiques
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        html.Div([
                                            html.I(className="fas fa-thermometer-half me-2", style={'color': '#4CAF50'}),
                                            html.Strong("Cliniques")
                                        ], className="mb-2"),
                                        html.P("Pression artérielle, Cholestérol, Glycémie", className="small text-muted mb-0")
                                    ], className="p-3", 
                                       style={'background': 'white', 'borderRadius': '10px', 
                                             'border': '2px solid #4CAF50', 'borderLeft': '5px solid #4CAF50'})
                                ], xs=12, md=6, className="mb-2"),
                                
                                dbc.Col([
                                    html.Div([
                                        html.Div([
                                            html.I(className="fas fa-heartbeat me-2", style={'color': '#FF6B35'}),
                                            html.Strong("Cardiologiques")
                                        ], className="mb-2"),
                                        html.P("Douleur thoracique, ECG, Fréquence cardiaque max", className="small text-muted mb-0")
                                    ], className="p-3", 
                                       style={'background': 'white', 'borderRadius': '10px', 
                                             'border': '2px solid #FF6B35', 'borderLeft': '5px solid #FF6B35'})
                                ], xs=12, md=6, className="mb-2"),
                            ]),
                            
                            # LIGNE 3: Tests d'effort (À GAUCHE)
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        html.Div([
                                            html.I(className="fas fa-running me-2", style={'color': '#FFC107'}),
                                            html.Strong("Tests d'effort")
                                        ], className="mb-2"),
                                        html.P("Angine induite, Dépression ST, Pente ST", className="small text-muted mb-0")
                                    ], className="p-3", 
                                       style={'background': 'white', 'borderRadius': '10px', 
                                             'border': '2px solid #FFC107', 'borderLeft': '5px solid #FFC107'})
                                ], xs=12, md=6, className="mb-2"),
                            ])
                            
                        ], style={'background': '#FFF8F3', 'padding': '1.5rem', 
                                'borderRadius': '12px', 'border': '3px solid #FFD4B8'})
                    ], xs=12, md=6, className="mb-3"),
                ])
                
            ], className="card p-4")
        ], width=12, className="mb-4")
    ]),
    
    # ========================================================================
    # MÉTHODOLOGIE
    # ========================================================================
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3([
                    html.I(className="fas fa-cogs me-2"),
                    "Méthodologie"
                ], className="text-orange mb-4 text-center"),
                
                dbc.Row([
                    # Étape 1 - Exploration
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.Span("1", className="badge", 
                                        style={'fontSize': '2rem', 'padding': '0.8rem 1.2rem',
                                              'background': 'linear-gradient(135deg, #2196F3 0%, #1976D2 100%)'}),
                            ], className="text-center mb-3"),
                            html.H5("Exploration", className="text-center mb-2", style={'color': '#2196F3'}),
                            html.P("Analyse exploratoire et visualisation des données pour comprendre les patterns.",
                                  className="text-center small text-muted")
                        ], className="p-3", 
                           style={'background': 'linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%)', 
                                 'borderRadius': '15px', 'border': '3px solid #2196F3',
                                 'boxShadow': '0 4px 8px rgba(33, 150, 243, 0.3)', 'height': '100%'})
                    ], xs=12, md=6, lg=3, className="mb-3"),
                    
                    # Étape 2 - Prétraitement
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.Span("2", className="badge", 
                                        style={'fontSize': '2rem', 'padding': '0.8rem 1.2rem',
                                              'background': 'linear-gradient(135deg, #4CAF50 0%, #388E3C 100%)'}),
                            ], className="text-center mb-3"),
                            html.H5("Prétraitement", className="text-center mb-2", style={'color': '#4CAF50'}),
                            html.P("Nettoyage, normalisation (RobustScaler), et préparation des données.",
                                  className="text-center small text-muted")
                        ], className="p-3", 
                           style={'background': 'linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%)', 
                                 'borderRadius': '15px', 'border': '3px solid #4CAF50',
                                 'boxShadow': '0 4px 8px rgba(76, 175, 80, 0.3)', 'height': '100%'})
                    ], xs=12, md=6, lg=3, className="mb-3"),
                    
                    # Étape 3 - Modélisation
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.Span("3", className="badge", 
                                        style={'fontSize': '2rem', 'padding': '0.8rem 1.2rem',
                                              'background': 'linear-gradient(135deg, #FF6B35 0%, #F44336 100%)'}),
                            ], className="text-center mb-3"),
                            html.H5("Modélisation", className="text-center mb-2", style={'color': '#FF6B35'}),
                            html.P("Test de 6 algorithmes ML avec validation croisée 5-fold et optimisation.",
                                  className="text-center small text-muted")
                        ], className="p-3", 
                           style={'background': 'linear-gradient(135deg, #FFE8D6 0%, #FFCCBC 100%)', 
                                 'borderRadius': '15px', 'border': '3px solid #FF6B35',
                                 'boxShadow': '0 4px 8px rgba(255, 107, 53, 0.3)', 'height': '100%'})
                    ], xs=12, md=6, lg=3, className="mb-3"),
                    
                    # Étape 4 - Prédiction
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.Span("4", className="badge", 
                                        style={'fontSize': '2rem', 'padding': '0.8rem 1.2rem',
                                              'background': 'linear-gradient(135deg, #9C27B0 0%, #7B1FA2 100%)'}),
                            ], className="text-center mb-3"),
                            html.H5("Prédiction", className="text-center mb-2", style={'color': '#9C27B0'}),
                            html.P("Déploiement du meilleur modèle pour des prédictions en temps réel.",
                                  className="text-center small text-muted")
                        ], className="p-3", 
                           style={'background': 'linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 100%)', 
                                 'borderRadius': '15px', 'border': '3px solid #9C27B0',
                                 'boxShadow': '0 4px 8px rgba(156, 39, 176, 0.3)', 'height': '100%'})
                    ], xs=12, md=6, lg=3, className="mb-3"),
                ])
                
            ], className="card p-4")
        ], width=12, className="mb-4")
    ])
    
], fluid=True, className="py-4")
