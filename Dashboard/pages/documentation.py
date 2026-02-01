
from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5([
                    html.I(className="fas fa-book me-2"),
                    "Documentation du Projet"
                ], className="mb-0")),
                dbc.CardBody([
                    html.H4("📊 Description du Dataset", className="text-primary mb-3"),
                    html.P("""
                    Ce projet utilise le Heart Disease Dataset de l'UCI Machine Learning Repository.
                    Le dataset contient 297 observations après nettoyage, avec 13 variables prédictives.
                    """),
                    
                    html.Hr(),
                    
                    html.H4("🎯 Objectif du Projet", className="text-primary mb-3"),
                    html.P("""
                    Développer un système d'aide à la décision pour prédire la présence de 
                    maladies cardiaques chez les patients, basé sur des indicateurs cliniques.
                    """),
                    
                    html.Hr(),
                    
                    html.H4("📈 Méthodologie", className="text-primary mb-3"),
                    html.Ol([
                        html.Li("Preprocessing: Nettoyage et encodage"),
                        html.Li("Feature Engineering: Scaling avec RobustScaler"),
                        html.Li("Modélisation: Test de 12 algorithmes"),
                        html.Li("Optimisation: GridSearch sur les meilleurs modèles"),
                        html.Li("Validation: Stratified K-Fold (5 folds)")
                    ]),
                    
                    html.Hr(),
                    
                    html.H4("🏆 Résultats", className="text-primary mb-3"),
                    dbc.Alert([
                        html.H5("Meilleur Modèle: Nu SVC", className="alert-heading"),
                        html.P("• Accuracy: 88.3%"),
                        html.P("• ROC-AUC: 0.94"),
                        html.P("• Recall: 81.8%"),
                        html.P("• Precision: 86.2%")
                    ], color="success"),
                    
                    html.Hr(),
                    
                    html.H4("⚠️ Limites & Avertissements", className="text-primary mb-3"),
                    dbc.Alert([
                        html.Ul([
                            html.Li("Dataset de taille limitée (297 patients)"),
                            html.Li("Ne remplace PAS le diagnostic médical professionnel"),
                            html.Li("À utiliser comme AIDE à la décision uniquement"),
                            html.Li("Nécessite validation continue avec nouvelles données")
                        ])
                    ], color="warning")
                ])
            ], className="shadow-sm")
        ])
    ])
], fluid=True)
