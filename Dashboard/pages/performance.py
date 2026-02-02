
"""
===============================================================================
PAGE MODÉLISATION
===============================================================================
Modèles, Top 3, et performances - Chargement automatique
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import sys
sys.path.append('..')
from ..utils import load_data, load_optimized_models, load_metrics, COLORS

dash.register_page(__name__, path='/modelisation', name='Modélisation')

# ============================================================================
# CHARGEMENT AUTOMATIQUE AU DÉMARRAGE
# ============================================================================

# Charger les données
metrics = load_metrics()

df_global = load_data()
results_global = load_optimized_models()
model_names_global = [k for k in results_global.keys() if k != '_metadata']
print("Modèles entraînés et prêts !\n")

# ============================================================================
# LAYOUT
# ============================================================================

layout = dbc.Container([
    
    # En-tête
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2([
                    html.I(className="fas fa-brain me-3"),
                    "Modélisation Machine Learning"
                ], className="text-center text-orange mb-3"),
                html.P("Comparaison et sélection du meilleur modèle (Recall priorisé)", 
                      className="text-center lead"),
            ], className="card p-4")
        ], width=12)
    ], className="mb-4"),
    
    # ========================================================================
    # SECTION 1: MODÈLES UTILISÉS
    # ========================================================================
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4([
                    html.I(className="fas fa-list-ul me-2"),
                    "Modèles Utilisés"
                ], className="text-orange mb-4"),
                
                # 6 modèles en grille
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.I(className="fas fa-brain text-orange fa-3x mb-2"),
                            html.H6("Neural Network", className="mb-2"),
                            html.P("Neuronal Network", className="small text-muted mb-0")
                        ], className="text-center p-3", 
                           style={'background': '#FFF8F3', 'borderRadius': '12px', 
                                 'border': '2px solid #FFD4B8', 'height': '150px'})
                    ], xs=6, md=4, lg=2, className="mb-3"),
                    
                    dbc.Col([
                        html.Div([
                            html.I(className="fas fa-tree text-orange fa-3x mb-2"),
                            html.H6("Decision Tree", className="mb-2"),
                            html.P("Arbre de décision", className="small text-muted mb-0")
                        ], className="text-center p-3", 
                           style={'background': '#FFF8F3', 'borderRadius': '12px', 
                                 'border': '2px solid #FFD4B8', 'height': '150px'})
                    ], xs=6, md=4, lg=2, className="mb-3"),
                    
                    dbc.Col([
                        html.Div([
                            html.I(className="fas fa-project-diagram text-orange fa-3x mb-2"),
                            html.H6("Random Forest", className="mb-2"),
                            html.P("Ensemble d'arbres", className="small text-muted mb-0")
                        ], className="text-center p-3", 
                           style={'background': '#FFF8F3', 'borderRadius': '12px', 
                                 'border': '2px solid #FFD4B8', 'height': '150px'})
                    ], xs=6, md=4, lg=2, className="mb-3"),
                    
                    dbc.Col([
                        html.Div([
                            html.I(className="fas fa-vector-square text-orange fa-3x mb-2"),
                            html.H6("Nu SVC", className="mb-2"),
                            html.P("Support Vector Classifier", className="small text-muted mb-0")
                        ], className="text-center p-3", 
                           style={'background': '#FFF8F3', 'borderRadius': '12px', 
                                 'border': '2px solid #FFD4B8', 'height': '150px'})
                    ], xs=6, md=4, lg=2, className="mb-3"),
                    
                    dbc.Col([
                        html.Div([
                            html.I(className="fas fa-microchip text-orange fa-3x mb-2"),
                            html.H6("Naive Bayes", className="mb-2"),
                            html.P("Probabilités bayésiennes", className="small text-muted mb-0")
                        ], className="text-center p-3", 
                           style={'background': '#FFF8F3', 'borderRadius': '12px', 
                                 'border': '2px solid #FFD4B8', 'height': '150px'})
                    ], xs=6, md=4, lg=2, className="mb-3"),
                    
                    dbc.Col([
                        html.Div([
                            html.I(className="fas fa-users-cog text-orange fa-3x mb-2"),
                            html.H6("Voting Classifier", className="mb-2"),
                            html.P("Ensemble de modèles", className="small text-muted mb-0")
                        ], className="text-center p-3", 
                           style={'background': '#FFF8F3', 'borderRadius': '12px', 
                                 'border': '2px solid #FFD4B8', 'height': '150px'})
                    ], xs=6, md=4, lg=2, className="mb-3"),
                    

                ]),
                
                html.Hr(className="my-4", style={'borderTop': '2px solid #FFD4B8'}),
                
                # Méthodologie - TITRE CENTRÉ + 3 COLONNES
                html.H5("Méthodologie", className="text-orange mb-4 text-center"),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-database text-orange me-2"),
                                html.Strong("Données")
                            ], className="mb-2 text-center"),
                            html.Ul([
                                html.Li("297 patients"),
                                html.Li("13 features médicales"),
                                html.Li("Cible binaire (sain/malade)"),
                            ], className="small")
                        ], style={'background': '#FFF8F3', 'padding': '1rem', 
                                'borderRadius': '12px', 'border': '2px solid #FFD4B8'})
                    ], xs=12, md=4, className="mb-3"),
                    
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-cog text-orange me-2"),
                                html.Strong("Prétraitement")
                            ], className="mb-2 text-center"),
                            html.Ul([
                                html.Li("Normalisation: RobustScaler"),
                                html.Li("Split: 75% train / 25% test"),
                                html.Li("Stratification par classe"),
                            ], className="small")
                        ], style={'background': '#FFF8F3', 'padding': '1rem', 
                                'borderRadius': '12px', 'border': '2px solid #FFD4B8'})
                    ], xs=12, md=4, className="mb-3"),
                    
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-chart-bar text-orange me-2"),
                                html.Strong("Validation")
                            ], className="mb-2 text-center"),
                            html.Ul([
                                html.Li("Cross-validation: 5-fold"),
                                html.Li([html.Strong("Métrique: Recall", 
                                       style={'color': '#FF6B35'})]),
                                html.Li("Recall crucial en médecine"),
                            ], className="small")
                        ], style={'background': '#FFF8F3', 'padding': '1rem', 
                                'borderRadius': '12px', 'border': '2px solid #FFD4B8'})
                    ], xs=12, md=4, className="mb-3"),
                ]),
                
            ], className="card p-4")
        ], width=12, className="mb-4")
    ]),
    
    # ========================================================================
    # SECTION 2: TOP 3 MODÈLES + TABLEAU COMPLET
    # ========================================================================
    dbc.Row([
        # GAUCHE: Top 3 avec filtre
        dbc.Col([
            html.Div([
                html.H4([
                    html.I(className="fas fa-trophy me-2"),
                    "Top 3 Meilleurs Modèles"
                ], className="text-orange mb-3"),
                
                # Filtre métrique
                html.Div([
                    html.Label("Trier par:", className="form-label fw-bold"),
                    dcc.Dropdown(
                        id='metric-filter',
                        options=[
                            {'label': 'Accuracy', 'value': 'accuracy'},
                            {'label': 'Precision', 'value': 'precision'},
                            {'label': 'Recall (utilisé)', 'value': 'recall'},
                            {'label': 'F1-Score', 'value': 'f1_score'},
                        ],
                        value='recall',
                        clearable=False
                    ),
                    html.Small("Note: Recall est utilisé pour le modèle final", 
                             className="text-muted fst-italic")
                ], className="mb-4"),
                
                # Podium
                html.Div(id='top3-podium')
                
            ], className="card p-4", style={'height': '420px'})
        ], xs=12, lg=6, className="mb-4"),
        
        # DROITE: Tableau comparatif TOUS LES MODÈLES
        dbc.Col([
            html.Div([
                html.H4([
                    html.I(className="fas fa-table me-2"),
                    "Comparaison Tous les Modèles"
                ], className="text-orange mb-3"),
                
                html.Div(id='comparison-table-all', style={'maxHeight': '650px', 'overflowY': 'auto'})
                
            ], className="card p-4", style={'height': '420px'})
        ], xs=12, lg=6, className="mb-4"),
    ]),
    
    # ========================================================================
    # SECTION 3: GRAPHIQUES RADAR + BARRES FILTREES (côte à côte)
    # ========================================================================
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H5([html.I(className="fas fa-chart-area me-2"), "Graphique Radar"], 
                       className="text-orange mb-3"),
                
                # FILTRES RADAR
                dbc.Row([
                    dbc.Col([
                        html.Label("Nombre de modèles:", className="form-label small"),
                        dcc.Dropdown(
                            id='radar-num-models',
                            options=[
                                {'label': 'Top 3', 'value': 3},
                                {'label': 'Top 5', 'value': 5},
                                {'label': 'Tous', 'value': 'all'},
                            ],
                            value=3,
                            clearable=False
                        ),
                    ], xs=12, md=6, className="mb-2"),
                    
                    dbc.Col([
                        html.Label("Métrique de tri:", className="form-label small"),
                        dcc.Dropdown(
                            id='radar-sort-metric',
                            options=[
                                {'label': 'Accuracy', 'value': 'accuracy'},
                                {'label': 'Precision', 'value': 'precision'},
                                {'label': 'Recall', 'value': 'recall'},
                                {'label': 'F1-Score', 'value': 'f1_score'},
                            ],
                            value='recall',
                            clearable=False
                        ),
                    ], xs=12, md=6, className="mb-2"),
                ]),
                
                dcc.Graph(id='radar-chart')
            ], className="card p-4", style={'height': '600px'})
        ], xs=12, md=6, className="mb-4"),
        
        dbc.Col([
            html.Div([
                html.H5([html.I(className="fas fa-sliders-h me-2"), "Comparaison Filtrée"], 
                       className="text-orange mb-3"),
                
                # 3 FILTRES
                dbc.Row([
                    dbc.Col([
                        html.Label("Nombre de modèles:", className="form-label small"),
                        dcc.Dropdown(
                            id='bar-num-models',
                            options=[
                                {'label': 'Top 3', 'value': 3},
                                {'label': 'Top 5', 'value': 5},
                                {'label': 'Tous', 'value': 'all'},
                            ],
                            value=3,
                            clearable=False
                        ),
                    ], xs=12, md=4, className="mb-2"),
                    
                    dbc.Col([
                        html.Label("Type de modèle:", className="form-label small"),
                        dcc.Dropdown(
                            id='bar-model-type',
                            options=[
                                {'label': 'Tous', 'value': 'all'},
                                {'label': 'Simples', 'value': 'simple'},
                                {'label': 'Ensembles', 'value': 'ensemble'},
                            ],
                            value='all',
                            clearable=False
                        ),
                    ], xs=12, md=4, className="mb-2"),
                    
                    dbc.Col([
                        html.Label("Métriques:", className="form-label small"),
                        dcc.Dropdown(
                            id='bar-metrics',
                            options=[
                                {'label': 'Toutes', 'value': 'all'},
                                {'label': 'Accuracy', 'value': 'accuracy'},
                                {'label': 'Precision', 'value': 'precision'},
                                {'label': 'Recall', 'value': 'recall'},
                                {'label': 'F1-Score', 'value': 'f1_score'},
                            ],
                            value='all',
                            clearable=False
                        ),
                    ], xs=12, md=4, className="mb-2"),
                ]),
                
                dcc.Graph(id='bar-chart')
            ], className="card p-4", style={'height': '600px'})
        ], xs=12, md=6, className="mb-4"),
    ]),
    
    # ========================================================================
    # SECTION 4: ROC FILTRÉE + MATRICE CONFUSION FILTRÉE (côte à côte)
    # ========================================================================
    dbc.Row([
        # GAUCHE: ROC avec filtre variable
        dbc.Col([
            html.Div([
                html.H5([html.I(className="fas fa-chart-line me-2"), "Courbe ROC"], 
                       className="text-orange mb-3"),
                
                html.Label("Filtrer par variable:", className="form-label"),
                dcc.Dropdown(
                    id='roc-variable-filter',
                    options=[
                        {'label': 'Tous les modèles', 'value': 'all'},
                        {'label': 'Top 3 uniquement', 'value': 'top3'},
                    ],
                    value='top3',
                    clearable=False,
                    className="mb-3"
                ),
                
                dcc.Graph(id='roc-curve')
            ], className="card p-4", style={'height': '550px'})
        ], xs=12, md=6, className="mb-4"),
        
        # DROITE: Matrice confusion avec filtre modèle
        dbc.Col([
            html.Div([
                html.H5([html.I(className="fas fa-th me-2"), "Matrice de Confusion"], 
                       className="text-orange mb-3"),
                
                html.Label("Filtrer par modèle:", className="form-label"),
                dcc.Dropdown(
                    id='cm-model-filter',
                    options=[{'label': name, 'value': name} for name in model_names_global],
                    value=model_names_global[0] if model_names_global else None,
                    clearable=False,
                    className="mb-3"
                ),
                
                dcc.Graph(id='confusion-matrix')
            ], className="card p-4", style={'height': '550px'})
        ], xs=12, md=6, className="mb-4"),
    ]),
    
    # ========================================================================
    # SECTION 5: VALIDATION CROISÉE + ANALYSE (côte à côte)
    # ========================================================================
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H5([html.I(className="fas fa-sync-alt me-2"), "Validation Croisée"], 
                       className="text-orange mb-3"),
                dcc.Graph(id='cv-scores')
            ], className="card p-4", style={'height': '500px'})
        ], xs=12, md=6, className="mb-4"),
        
        dbc.Col([
            html.Div([
                html.H5([html.I(className="fas fa-microscope me-2"), "Analyse de Performance"], 
                       className="text-orange mb-3"),
                html.Div(id='performance-analysis')
            ], className="card p-4", style={'height': '500px', 'overflowY': 'auto'})
        ], xs=12, md=6, className="mb-4"),
    ]),
    
    # ========================================================================
    # SECTION 6: TABLEAU GLOBAL DE COMPARAISON (EN BAS)
    # ========================================================================
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4([
                    html.I(className="fas fa-list-alt me-2"),
                    "Tableau Récapitulatif Global"
                ], className="text-orange mb-3"),
                
                html.Div(id='global-comparison-table')
                
            ], className="card p-4")
        ], width=12, className="mb-4")
    ]),
    
], fluid=True)


# ============================================================================
# CALLBACKS
# ============================================================================

@callback(
    [
        Output('top3-podium', 'children'),
        Output('comparison-table-all', 'children'),
        Output('global-comparison-table', 'children'),
    ],
    Input('metric-filter', 'value')
)
def update_top3_and_tables(metric):
    """Mettre à jour le Top 3 et les tableaux selon la métrique"""
    
    # Trier selon la métrique
    sorted_models = sorted(
        [(name, results_global[name]) for name in model_names_global],
        key=lambda x: x[1][metric],
        reverse=True
    )
    
    # Top 3
    top3 = sorted_models[:3]
    top3_names = [name for name, _ in top3]
    
    # ========================================================================
    # PODIUM - Textes réduits
    # ========================================================================
    podium = dbc.Row([
        # 2ème place
        dbc.Col([
            html.Div([
                html.I(className="fas fa-medal fa-3x mb-2", style={'color': '#C0C0C0'}),
                html.H6("2ème", className="mb-2", style={'fontSize': '0.9rem'}),
                html.P(top3_names[1], className="mb-2 fw-bold", style={'fontSize': '0.95rem'}),
                html.P(f"{top3[1][1][metric]:.1%}", 
                      className="mb-0", style={'fontSize': '1.1rem', 'fontWeight': 'bold'}),
            ], className="text-center p-3", 
               style={'background': 'linear-gradient(135deg, #E8E8E8 0%, #C0C0C0 100%)',
                     'borderRadius': '16px', 'color': 'white', 'minHeight': '160px'})
        ], xs=12, md=4, className="mb-3 mt-4"),
        
        # 1ère place
        dbc.Col([
            html.Div([
                html.I(className="fas fa-crown fa-4x mb-2", style={'color': '#FFD700'}),
                html.H5("1er", className="mb-2", style={'fontSize': '1.1rem'}),
                html.P(top3_names[0], className="mb-2 fw-bold", style={'fontSize': '1.05rem'}),
                html.P(f"{top3[0][1][metric]:.1%}", 
                      className="mb-0", style={'fontSize': '1.3rem', 'fontWeight': 'bold'}),
            ], className="text-center p-3", 
               style={'background': 'linear-gradient(135deg, #FFD700 0%, #FFA500 100%)',
                     'borderRadius': '16px', 'color': 'white', 'minHeight': '200px',
                     'boxShadow': '0 8px 24px rgba(255, 215, 0, 0.5)'})
        ], xs=12, md=4, className="mb-3"),
        
        # 3ème place
        dbc.Col([
            html.Div([
                html.I(className="fas fa-medal fa-3x mb-2", style={'color': '#CD7F32'}),
                html.H6("3ème", className="mb-2", style={'fontSize': '0.9rem'}),
                html.P(top3_names[2], className="mb-2 fw-bold", style={'fontSize': '0.95rem'}),
                html.P(f"{top3[2][1][metric]:.1%}", 
                      className="mb-0", style={'fontSize': '1.1rem', 'fontWeight': 'bold'}),
            ], className="text-center p-3", 
               style={'background': 'linear-gradient(135deg, #CD853F 0%, #8B4513 100%)',
                     'borderRadius': '16px', 'color': 'white', 'minHeight': '160px'})
        ], xs=12, md=4, className="mb-3 mt-4"),
    ])
    
    # ========================================================================
    # TABLEAU TOUS LES MODÈLES
    # ========================================================================
    table_all_data = pd.DataFrame({
        'Modèle': [name for name, _ in sorted_models],
        'Accuracy': [f"{res['accuracy']:.1%}" for _, res in sorted_models],
        'Precision': [f"{res['precision']:.1%}" for _, res in sorted_models],
        'Recall': [f"{res['recall']:.1%}" for _, res in sorted_models],
        'F1-Score': [f"{res['f1_score']:.1%}" for _, res in sorted_models],
    })
    
    table_all = dbc.Table.from_dataframe(
        table_all_data, 
        striped=True, bordered=True, hover=True, responsive=True, size='sm'
    )
    
    # ========================================================================
    # TABLEAU GLOBAL AVEC SENSIBILITÉ - TRIÉ PAR F1-SCORE
    # ========================================================================
    # Trier par F1-Score pour le tableau global
    sorted_by_f1 = sorted(
        [(name, results_global[name]) for name in model_names_global],
        key=lambda x: x[1]['recall'],
        reverse=True
    )
    
    global_table_data = pd.DataFrame({
        'Rang': [f"{i+1}" for i in range(len(sorted_by_f1))],
        'Modèle': [name for name, _ in sorted_by_f1],
        'Accuracy': [f"{res['accuracy']:.3f}" for _, res in sorted_by_f1],
        'Precision': [f"{res['precision']:.3f}" for _, res in sorted_by_f1],
        'Recall': [f"{res['recall']:.3f}" for _, res in sorted_by_f1],
        'Sensibilité': [f"{res['recall']:.3f}" for _, res in sorted_by_f1],  # Sensibilité = Recall
        'F1-Score': [f"{res['f1_score']:.3f}" for _, res in sorted_by_f1],
    })
    
    global_table = dbc.Table.from_dataframe(
        global_table_data,
        striped=True, bordered=True, hover=True, responsive=True
    )
    
    return podium, table_all, global_table


@callback(
    Output('radar-chart', 'figure'),
    [
        Input('radar-num-models', 'value'),
        Input('radar-sort-metric', 'value'),
    ]
)
def update_radar_chart(num_models, sort_metric):
    """Graphique radar avec filtres"""
    
    # Trier selon la métrique
    sorted_models = sorted(
        [(name, results_global[name]) for name in model_names_global],
        key=lambda x: x[1][sort_metric],
        reverse=True
    )
    
    # Sélectionner le nombre de modèles
    if num_models != 'all':
        models_to_show = sorted_models[:num_models]
    else:
        models_to_show = sorted_models
    
    # ========================================================================
    # RADAR
    # ========================================================================
    fig_radar = go.Figure()
    metrics_list = ['accuracy', 'precision', 'recall', 'f1_score']
    
    # Couleurs dynamiques selon le nombre
    if num_models == 3:
        colors = ['#FFD700', '#C0C0C0', '#CD7F32']
    elif num_models == 5:
        colors = ['#FFD700', '#C0C0C0', '#CD7F32', '#FF6B35', '#4CAF50']
    else:
        colors = px.colors.qualitative.Plotly
    
    for i, (name, res) in enumerate(models_to_show):
        values = [res[m] for m in metrics_list]
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=[m.replace('_', ' ').title() for m in metrics_list] + [metrics_list[0].replace('_', ' ').title()],
            fill='toself',
            name=name,
            line=dict(color=colors[i % len(colors)], width=3),
            fillcolor=colors[i % len(colors)],
            opacity=0.3
        ))
    
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1], tickformat='.0%')),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        height=450
    )
    
    return fig_radar


@callback(
    Output('bar-chart', 'figure'),
    [
        Input('bar-num-models', 'value'),
        Input('bar-model-type', 'value'),
        Input('bar-metrics', 'value'),
        Input('metric-filter', 'value'),
    ]
)
def update_bar_chart(num_models, model_type, metrics_choice, sort_metric):
    """Graphique barres avec 3 filtres"""
    
    # Trier selon la métrique de tri
    sorted_models = sorted(
        [(name, results_global[name]) for name in model_names_global],
        key=lambda x: x[1][sort_metric],
        reverse=True
    )
    
    # Filtre 1: Nombre de modèles
    if num_models != 'all':
        sorted_models = sorted_models[:num_models]
    
    # Filtre 2: Type de modèle
    if model_type == 'simple':
        sorted_models = [(n, r) for n, r in sorted_models if n not in ['Voting Classifier', 'Random Forest']]
    elif model_type == 'ensemble':
        sorted_models = [(n, r) for n, r in sorted_models if n in ['Voting Classifier', 'Random Forest']]
    
    # Préparer les données
    model_names = [name for name, _ in sorted_models]
    
    fig = go.Figure()
    
    # Filtre 3: Métriques
    if metrics_choice == 'all':
        metrics_to_show = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
        metric_colors = {'Accuracy': '#2196F3', 'Precision': '#4CAF50', 'Recall': '#FF6B35', 'F1-Score': '#FFC107'}
    else:
        metrics_to_show = [metrics_choice.replace('_', ' ').title()]
        metric_colors = {metrics_choice.replace('_', ' ').title(): '#FF6B35'}
    
    for met_display in metrics_to_show:
        met_key = met_display.lower().replace(' ', '_').replace('-', '_')
        values = [res[met_key] for _, res in sorted_models]
        
        fig.add_trace(go.Bar(
            x=model_names,
            y=values,
            name=met_display,
            marker=dict(color=metric_colors[met_display]),
            text=[f'{v:.1%}' for v in values],
            textposition='outside',
            textfont=dict(size=11)
        ))
    
    fig.update_layout(
        barmode='group',
        xaxis_title='<b>Modèle</b>',
        yaxis_title='<b>Score</b>',
        yaxis=dict(tickformat='.0%', range=[0, 1.15]),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,1)',
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    
    return fig


@callback(
    Output('roc-curve', 'figure'),
    Input('roc-variable-filter', 'value')
)
def update_roc(filter_val):
    """Courbe ROC filtrée"""
    
    fig = go.Figure()
    
    if filter_val == 'top3':
        # Top 3 par F1
        sorted_by_f1 = sorted(
            [(model_name, metrics['roc'][model_name]) for model_name in metrics['roc']],
            reverse=True
        )[:3]
        models_to_plot = sorted_by_f1
        colors = ['#FFD700', '#C0C0C0', '#CD7F32']
    else:
        # Tous
        models_to_plot = [(model_name, metrics['roc'][model_name]) for model_name in metrics['roc']]
        colors = px.colors.qualitative.Plotly
    
    from sklearn.metrics import roc_curve, roc_auc_score
    
    for i, (model_name, data) in enumerate(models_to_plot):
        fig.add_trace(go.Scatter(
            x=data['fpr'],
            y=data['tpr'],
            mode='lines',
            name=f"{model_name} (AUC={data['auc']:.3f})",
            line=dict(color=colors[i % len(colors)], width=3)
        ))
    
    # Ligne de référence
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode='lines',
        name='Aléatoire',
        line=dict(color='gray', width=2, dash='dash')
    ))
    
    fig.update_layout(
        xaxis_title='<b>Taux Faux Positifs (FPR)</b>',
        yaxis_title='<b>Taux Vrais Positifs (TPR)</b>',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,1)',
        height=400,
        xaxis=dict(range=[0, 1], gridcolor='#f0f0f0'),
        yaxis=dict(range=[0, 1], gridcolor='#f0f0f0'),
        legend=dict(yanchor="bottom", y=0.02, xanchor="right", x=0.98)
    )
    
    return fig


@callback(
    Output('confusion-matrix', 'figure'),
    Input('cm-model-filter', 'value')
)
def update_confusion_matrix(model_name):
    """Matrice de confusion filtrée par modèle"""
    
    if model_name is None or model_name not in results_global:
        return go.Figure()
    
    cm = results_global[model_name]['confusion_matrix']
    
    annotations = []
    total = cm.sum()
    for i in range(2):
        for j in range(2):
            annotations.append(f"<b>{cm[i, j]}</b><br>({cm[i, j]/total*100:.1f}%)")
    
    fig = ff.create_annotated_heatmap(
        z=cm,
        x=['<b>Prédit Sain</b>', '<b>Prédit Malade</b>'],
        y=['<b>Réel Sain</b>', '<b>Réel Malade</b>'],
        annotation_text=np.array(annotations).reshape(2, 2),
        colorscale=[[0, '#4CAF50'], [0.5, '#FFE8D6'], [1, '#FF6B35']],
        showscale=True,
        font_colors=['black']
    )
    
    fig.update_layout(
        title={'text': f'<b>{model_name}</b>', 'x': 0.5, 'xanchor': 'center'},
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        xaxis=dict(side='bottom')
    )
    
    return fig


@callback(
    Output('cv-scores', 'figure'),
    Input('metric-filter', 'value')
)
def update_cv_scores(_):
    """Validation croisée"""
    df_cv = metrics['cv']
    
    names_with_cv = df_cv[df_cv['Fold'] != 'Moyenne'].copy()
    names_with_cv['Fold'] = names_with_cv['Fold'].astype(str)
    #means = [results_global[n]['cv_mean'] for n in names_with_cv]
    #stds = [results_global[n]['cv_std'] for n in names_with_cv]
    
    fig = go.Figure()
    
    # Ajouter traces pour chaque métrique
    metriques = ['Test_Accuracy', 'Test_Precision', 'Test_Recall', 'Test_F1']
    colors_map = {
        'Test_Accuracy': COLORS['primary'],
        'Test_Precision': COLORS['success'],
        'Test_Recall': COLORS['danger'],
        'Test_F1': COLORS['warning']
    }
    
    for metric in metriques:
        fig.add_trace(go.Scatter(
            x=names_with_cv['Fold'],
            y=names_with_cv[metric],
            #error_y=dict(type='data', array=stds, color='#333'),
            marker=dict(color=colors_map[metric]),
            name=metric.replace('Test_', ''),
            #text=[f'{m:.1%}<br>±{s:.2%}' for m, s in zip(means, stds)],
            #textposition='outside'
    ))
    
    fig.update_layout(
        xaxis_title='<b>Modèle</b>',
        yaxis_title='<b>Score CV (5-Fold)</b>',
        yaxis=dict(tickformat='.0%',range=[0, 1] if not names_with_cv['Fold'].empty else [0, 1]),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,1)',
        height=400
    )
    
    return fig


@callback(
    Output('performance-analysis', 'children'),
    Input('metric-filter', 'value')
)
def update_analysis(metric):
    """Analyse du meilleur modèle (par F1, peu importe le filtre)"""
    
    # Toujours basé sur F1
    sorted_by_f1 = sorted(
        [(name, results_global[name]) for name in model_names_global],
        key=lambda x: x[1]['recall'],
        reverse=True
    )
    
    best_name, best_res = sorted_by_f1[0]
    
    return [
        dbc.Alert([
            html.H6([
                html.I(className="fas fa-trophy me-2"),
                f"Modèle Final: {best_name}"
            ], className="mb-0")
        ], color="success", className="mb-3"),
        
        html.Div([
            html.H6("Métriques:", className="text-orange mb-2"),
            html.Ul([
                html.Li(f"Recall: {best_res['recall']:.1%} ⭐"),
                html.Li(f"Precision: {best_res['precision']:.1%}"),
                html.Li(f"F1-Score: {best_res['f1_score']:.1%}"),
                html.Li(f"Accuracy: {best_res['accuracy']:.1%}"),
            ], className="small"),
            
            html.Hr(),
            
            html.H6("Pourquoi ce modèle?", className="text-orange mb-2"),
            html.P([
                "Le ",
                html.Strong("Recall", style={'color': '#FF6B35'}),
                " est crucial dans ce contexte médical. ",
                f"Avec {best_res['recall']:.1%}, ce modèle détecte bien les patients malades.",
                " Cela réduit le risque de faux négatifs (patients malades manqués)."
            ], className="small"),
            
            html.Hr(),
            
            html.H6("Interprétation Médicale:", className="text-orange mb-2"),
            html.P([
                f"Recall de {best_res['recall']:.1%} signifie que ",
                html.Strong(f"{best_res['recall']*100:.0f}% des patients malades sont détectés", 
                           style={'color': '#4CAF50'}),
                f". Seulement {(1-best_res['recall'])*100:.0f}% de faux négatifs (patients malades manqués)."
            ], className="small mb-0"),
        ])
    ]
