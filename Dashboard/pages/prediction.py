"""
===============================================================================
PAGE PRÉDICTION
===============================================================================
Interface de prédiction pour un patient individuel
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import sys
import io
import os
import datetime
from fpdf import FPDF
sys.path.append('..')
from utils import load_model, load_scaler, make_prediction

dash.register_page(__name__, path='/prediction', name='Prédiction')

# Charger modèle et scaler
model = load_model('models/best_model.pkl')
scaler = load_scaler('models/scaler.pkl')

# ============================================================================
# LAYOUT
# ============================================================================

layout = dbc.Container([
    
    # En-tête
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2([
                    html.I(className="fas fa-user-md me-3"),
                    "Prédiction Individuelle"
                ], className="text-center text-orange mb-3"),
                html.P("Entrez les informations du patient pour prédire le risque cardiaque",
                      className="text-center lead"),
            ], className="card p-4")
        ], width=12)
    ], className="mb-4"),
    
    # Formulaire & Résultats
    dbc.Row([
        # FORMULAIRE
        dbc.Col([
            html.Div([
                html.H4([html.I(className="fas fa-edit me-2"), "Informations Patient"], 
                       className="text-orange mb-4"),
                
                dbc.Form([
                    # Section 1: Démographie
                    html.H5([html.I(className="fas fa-user me-2"), "Démographie"], 
                           className="text-orange mt-3 mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Label("Âge:", className="form-label fw-bold"),
                            dbc.Input(id="pred-age", type="number", value=55, min=20, max=100),
                            html.Small("20-100 ans", className="text-muted")
                        ], xs=12, md=6, className="mb-3"),
                        
                        dbc.Col([
                            html.Label("Sexe:", className="form-label fw-bold"),
                            dcc.Dropdown(
                                id="pred-sexe",
                                options=[{'label': 'Homme', 'value': 1}, {'label': 'Femme', 'value': 0}],
                                value=1, clearable=False
                            ),
                        ], xs=12, md=6, className="mb-3"),
                    ]),
                    
                    html.Hr(style={'borderTop': '2px solid #FFD4B8'}),
                    
                    # Section 2: Paramètres vitaux
                    html.H5([html.I(className="fas fa-heartbeat me-2"), "Paramètres Vitaux"], 
                           className="text-orange mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Label("Pression Artérielle (mm Hg):", className="form-label fw-bold"),
                            dbc.Input(id="pred-trestbps", type="number", value=120, min=80, max=200),
                        ], xs=12, md=6, className="mb-3"),
                        
                        dbc.Col([
                            html.Label("Cholestérol (mg/dl):", className="form-label fw-bold"),
                            dbc.Input(id="pred-chol", type="number", value=250, min=100, max=600),
                        ], xs=12, md=6, className="mb-3"),
                    ]),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Label("Fréquence Cardiaque Max (bpm):", className="form-label fw-bold"),
                            dbc.Input(id="pred-thalach", type="number", value=150, min=60, max=220),
                        ], xs=12, md=6, className="mb-3"),
                        
                        dbc.Col([
                            html.Label("Glycémie à jeun > 120:", className="form-label fw-bold"),
                            dcc.Dropdown(
                                id="pred-fbs",
                                options=[{'label': 'Non', 'value': 0}, {'label': 'Oui', 'value': 1}],
                                value=0, clearable=False
                            ),
                        ], xs=12, md=6, className="mb-3"),
                    ]),
                    
                    html.Hr(style={'borderTop': '2px solid #FFD4B8'}),
                    
                    # Section 3: Tests cardiaques
                    html.H5([html.I(className="fas fa-stethoscope me-2"), "Tests Cardiaques"], 
                           className="text-orange mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Label("Type Douleur Thoracique:", className="form-label fw-bold"),
                            dcc.Dropdown(
                                id="pred-cp",
                                options=[
                                    {'label': 'Angine Typique', 'value': 1},
                                    {'label': 'Angine Atypique', 'value': 2},
                                    {'label': 'Non-Angineuse', 'value': 3},
                                    {'label': 'Asymptomatique', 'value': 4}
                                ],
                                value=4, clearable=False
                            ),
                        ], xs=12, md=6, className="mb-3"),
                        
                        dbc.Col([
                            html.Label("ECG Repos:", className="form-label fw-bold"),
                            dcc.Dropdown(
                                id="pred-restecg",
                                options=[
                                    {'label': 'Normal', 'value': 0},
                                    {'label': 'Anomalie ST-T', 'value': 1},
                                    {'label': 'Hypertrophie VG', 'value': 2}
                                ],
                                value=0, clearable=False
                            ),
                        ], xs=12, md=6, className="mb-3"),
                    ]),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Label("Angine Exercice:", className="form-label fw-bold"),
                            dcc.Dropdown(
                                id="pred-exang",
                                options=[{'label': 'Non', 'value': 0}, {'label': 'Oui', 'value': 1}],
                                value=0, clearable=False
                            ),
                        ], xs=12, md=6, className="mb-3"),
                        
                        dbc.Col([
                            html.Label("Dépression ST:", className="form-label fw-bold"),
                            dbc.Input(id="pred-oldpeak", type="number", value=1.0, min=0, max=10, step=0.1),
                        ], xs=12, md=6, className="mb-3"),
                    ]),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Label("Pente ST:", className="form-label fw-bold"),
                            dcc.Dropdown(
                                id="pred-slope",
                                options=[
                                    {'label': 'Ascendante', 'value': 1},
                                    {'label': 'Plate', 'value': 2},
                                    {'label': 'Descendante', 'value': 3}
                                ],
                                value=2, clearable=False
                            ),
                        ], xs=12, md=6, className="mb-3"),
                        
                        dbc.Col([
                            html.Label("Vaisseaux Majeurs (0-3):", className="form-label fw-bold"),
                            dbc.Input(id="pred-ca", type="number", value=0, min=0, max=3),
                        ], xs=12, md=6, className="mb-3"),
                    ]),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Label("Thalassémie:", className="form-label fw-bold"),
                            dcc.Dropdown(
                                id="pred-thal",
                                options=[
                                    {'label': 'Normal', 'value': 3},
                                    {'label': 'Défaut Fixe', 'value': 6},
                                    {'label': 'Défaut Réversible', 'value': 7}
                                ],
                                value=3, clearable=False
                            ),
                        ], xs=12, md=6, className="mb-3"),
                    ]),
                    
                    html.Hr(style={'borderTop': '2px solid #FFD4B8'}),
                    
                    # Boutons
                    dbc.Row([
                        dbc.Col([
                            dbc.Button([
                                html.I(className="fas fa-calculator me-2"),
                                "Prédire"
                            ], id="btn-predict", color="primary", size="lg", className="w-100"),
                        ], xs=12, md=6, className="mb-3"),
                        
                        dbc.Col([
                            dbc.Button([
                                html.I(className="fas fa-redo me-2"),
                                "Réinitialiser"
                            ], id="btn-reset", color="secondary", size="lg", className="w-100"),
                        ], xs=12, md=6, className="mb-3"),
                    ])
                ])
            ], className="card p-4")
        ], xs=12, lg=7, className="mb-4"),
        
        # RÉSULTATS
        dbc.Col([
            html.Div([
                html.H4([html.I(className="fas fa-chart-pie me-2"), "Résultats"], 
                       className="text-orange mb-4"),
                
                html.Div(id="prediction-output", className="text-center"),
                
                html.Div([
                    dcc.Graph(id="gauge-risk", config={'displayModeBar': False})
                ], className="mt-4"),
                
                html.Div(id="recommendations", className="mt-4"),
                
                # Bouton pour générer le PDF
                html.Div([
                    dbc.Button([
                        html.I(className="fas fa-file-pdf me-2"),
                        "Télécharger le Rapport PDF"
                    ], id="btn-pdf", color="danger", size="lg", className="w-100 mt-3"),
                ], id="pdf-button-container", style={'display': 'none'}),  # Caché par défaut
                
                # Store pour les données de prédiction (pour le PDF)
                dcc.Store(id="prediction-store"),
                
                # Composant pour télécharger le PDF
                dcc.Download(id="download-pdf"),
                
            ], className="card p-4", style={'position': 'sticky', 'top': '100px'})
        ], xs=12, lg=5, className="mb-4"),
    ]),
    
], fluid=True)

# Hidden components for state management and downloads
hidden_components = html.Div(
    [
        dcc.Store(id="prediction-store"),
        dcc.Download(id="download-pdf")
    ]
)

layout.children.append(hidden_components)

# ============================================================================
# CALLBACKS
# ============================================================================

@callback(
    [
        Output("pred-age", "value"),
        Output("pred-sexe", "value"),
        Output("pred-cp", "value"),
        Output("pred-trestbps", "value"),
        Output("pred-chol", "value"),
        Output("pred-fbs", "value"),
        Output("pred-restecg", "value"),
        Output("pred-thalach", "value"),
        Output("pred-exang", "value"),
        Output("pred-oldpeak", "value"),
        Output("pred-slope", "value"),
        Output("pred-ca", "value"),
        Output("pred-thal", "value"),
    ],
    Input("btn-reset", "n_clicks"),
    prevent_initial_call=True
)
def reset_form(n):
    return 55, 1, 4, 120, 250, 0, 0, 150, 0, 1.0, 2, 0, 3


@callback(
    [
        Output("prediction-output", "children"),
        Output("gauge-risk", "figure"),
        Output("recommendations", "children"),
        Output("prediction-store", "data"),
        Output("pdf-button-container", "style"),
    ],
    Input("btn-predict", "n_clicks"),
    [State(f'pred-{var}', 'value') for var in [
        'age', 'sexe', 'cp', 'trestbps', 'chol', 'fbs', 
        'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
    ]],
    prevent_initial_call=True
)
def predict_disease(n_clicks, âge, sexe, type_douleur_thoracique, pression_artérielle_repos, cholestérol, glycémie_à_jeun, 
                    électrocardiogramme_repos, fréquence_cardiaque_maximale, angine_induite_par_exercice, dépression_st, pente_st, nombre_vaisseaux_majeurs, thalassémie):
    
    features = {
        'age': âge, 'sex': sexe, 'cp': type_douleur_thoracique, 'trestbps': pression_artérielle_repos,
        'chol': cholestérol, 'fbs': glycémie_à_jeun, 'restecg': électrocardiogramme_repos, 'thalach': fréquence_cardiaque_maximale,
        'exang': angine_induite_par_exercice, 'oldpeak': dépression_st, 'slope': pente_st, 'ca': nombre_vaisseaux_majeurs, 'thal': thalassémie
    }
    
    # Créer DataFrame
    patient_df = pd.DataFrame({
        'âge': [âge],
        'sexe': [sexe],
        'type_douleur_thoracique': [type_douleur_thoracique],
        'pression_artérielle_repos': [pression_artérielle_repos],
        'cholestérol': [cholestérol],
        'glycémie_à_jeun': [glycémie_à_jeun],
        'électrocardiogramme_repos': [électrocardiogramme_repos],
        'fréquence_cardiaque_maximale': [fréquence_cardiaque_maximale],
        'angine_induite_par_exercice': [angine_induite_par_exercice],
        'dépression_st': [dépression_st],
        'pente_st': [pente_st],
        'nombre_vaisseaux_majeurs': [nombre_vaisseaux_majeurs],
        'thalassémie': [thalassémie]
    })
    
    # Prédiction
    prediction, probas, error = make_prediction(model, scaler, patient_df)
    
    if error:
        return (
            dbc.Alert(f"⚠️ {error}", color="danger"),
            dash.no_update,
            dash.no_update,
            dash.no_update,
            {'display': 'none'}  # Cacher le bouton PDF
    )
    
    # Affichage résultat
    if prediction == 1:
        alert_color = "danger"
        icon = "fas fa-exclamation-triangle"
        titre = "RISQUE ÉLEVÉ DE MALADIE CARDIAQUE"
        message = "Ce patient présente un risque élevé de maladie cardiaque."
    elif probas[1] > 0.35:
        alert_color = "warning"
        icon = "fas fa-exclamation-circle"
        titre = "RISQUE MODÉRÉ (CAS LIMITE)"
        message = "Probabilité proche du seuil. Examens complémentaires recommandés."
    else:
        alert_color = "success"
        icon = "fas fa-check-circle"
        titre = "RISQUE FAIBLE"
        message = "Ce patient présente un faible risque de maladie cardiaque."
    
    output = [
        html.I(
            className=f"fas fa-{'heart-broken' if prediction == 1 else 'heart'} fa-4x mb-3",
            style={'color': '#FF6B35' if prediction == 1 else '#4CAF50'}
        ),
        html.H2(titre, className="mb-2",
               style={'color': '#FF6B35' if prediction == 1 else '#4CAF50'}),
        html.P(f"Probabilité: {probas[1]:.1%}", className="lead mb-3"),
        dbc.Badge(f"Risque {titre.split(' ')[-1]}", color=alert_color, className="p-2", 
                 style={'fontSize': '1.1rem'})
    ]
    
     # Save to History
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    history_path = os.path.join(BASE_DIR, "data", "history.csv")
    log_data = patient_df.copy()
    log_data["prediction"] = prediction
    log_data["probability"] = probas[1] * 100
    log_data["risk_level"] = titre.split(' ')[-1]
    log_data["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # log_data est déjà un DataFrame
    if not os.path.exists(history_path):
        log_data.to_csv(history_path, index=False)
    else:
        log_data.to_csv(history_path, mode='a', header=False, index=False)
    
    # Jauge
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probas[1] * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Probabilité (%)", 'font': {'size': 18, 'color': '#FF6B35'}},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#FF6B35"},
            'steps': [
                {'range': [0, 30], 'color': '#E8F5E9'},
                {'range': [30, 60], 'color': '#FFF9C4'},
                {'range': [60, 100], 'color': '#FFEBEE'}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'value': 90}
        }
    ))
    fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=300)
    
    # Recommandations
    if prediction == 1:
        recs = html.Div([
            html.H5([html.I(className="fas fa-exclamation-circle me-2"), "Recommandations"], 
                   className="text-danger mb-3"),
            dbc.Alert([
                html.Ul([
                    html.Li("Consulter un cardiologue rapidement"),
                    html.Li("Tests cardiovasculaires approfondis"),
                    html.Li("Surveiller pression artérielle"),
                    html.Li("Adopter un régime sain"),
                    html.Li("Activité physique modérée"),
                ], className="mb-0")
            ], color="warning")
        ])
    else:
        recs = html.Div([
            html.H5([html.I(className="fas fa-check-circle me-2"), "Recommandations"], 
                   className="text-success mb-3"),
            dbc.Alert([
                html.Ul([
                    html.Li("Maintenir mode de vie sain"),
                    html.Li("Contrôles médicaux réguliers"),
                    html.Li("Surveiller cholestérol et tension"),
                    html.Li("Activité physique régulière"),
                    html.Li("Alimentation équilibrée"),
                ], className="mb-0")
            ], color="success")
        ])
    
    return output, fig_gauge, recs, log_data.to_dict('records')[0], {'display': 'block'}  # Afficher le bouton PDF

@callback(
    Output("download-pdf", "data"),
    Input("btn-pdf", "n_clicks"),
    State("prediction-store", "data"),
    prevent_initial_call=True
)
def generate_pdf_report(n_clicks, data):
    if not n_clicks or not data:
        return
        
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # Header
    pdf.set_text_color(0, 74, 173) # Primary Blue
    pdf.cell(0, 10, "HeartGuard Predict - Rapport d'Analyse", 0, 1, 'C')
    pdf.ln(10)
    
    # Date
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Date: {data.get('date', 'N/A')}", 0, 1, 'R')
    pdf.ln(5)
    
    # Patient Data
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(240, 248, 255)
    pdf.cell(0, 10, "Données Patient", 0, 1, 'L', 1)
    
    pdf.set_font("Arial", '', 11)
    info_str = f"Age: {data.get('âge')} | Sexe: {'Homme' if data.get('sexe')==1 else 'Femme'} | Pression Artérielle: {data.get('pression_artérielle_repos')} mmHg"
    pdf.cell(0, 10, info_str, 0, 1)
    info_str2 = f"Cholestérol: {data.get('cholestérol')} mg/dl | FC Max: {data.get('fréquence_cardiaque_maximale')} bpm"
    pdf.cell(0, 10, info_str2, 0, 1)
    pdf.ln(10)
    
    # Result
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Résultats de l'IA", 0, 1, 'L', 1)
    
    risk_level = data.get('risk_level', 'Inconnu')
    prob = data.get('probability', 0)
    pred = data.get('prediction', 0)
    
    pdf.set_font("Arial", 'B', 14)
    if pred == 1:
        pdf.set_text_color(220, 53, 69) # Red
        res_text = "RISQUE DE MALADIE CODECTÉ"
    else:
        pdf.set_text_color(25, 135, 84) # Green
        res_text = "RISQUE FAIBLE / SAIN"
        
    pdf.cell(0, 15, res_text, 0, 1, 'C')
    
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Probabilité: {prob}% | Niveau de Risque: {risk_level}", 0, 1, 'C')
    pdf.ln(10)
    
    # Advice
    pdf.set_font("Arial", 'I', 10)
    advice = "Ce rapport est généré automatiquement par intelligence artificielle. Il ne remplace pas un diagnostic médical professionnel. Veuillez consulter un cardiologue."
    pdf.multi_cell(0, 5, advice)
    
    return dcc.send_bytes(pdf.output(dest='S').encode('latin-1'), filename="rapport_cardiologique.pdf")
