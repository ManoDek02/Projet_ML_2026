
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from utils import load_data

# Charger les faux négatifs
try:
    df_fn = load_data('data/results/false_negatives_real_values.csv')
except:
    df_fn = pd.DataFrame()

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5([
                    html.I(className="fas fa-bug me-2 text-danger"),
                    "Analyse des Faux Négatifs"
                ], className="mb-0")),
                dbc.CardBody([
                    dbc.Alert([
                        html.I(className="fas fa-exclamation-triangle fa-2x mb-2"),
                        html.H5(f"{len(df_fn)} patients malades NON détectés"),
                        html.P("Ces cas nécessitent une attention particulière")
                    ], color="danger", className="text-center"),
                    
                    dash_table.DataTable(
                        data=df_fn.to_dict('records') if not df_fn.empty else [],
                        columns=[{'name': i, 'id': i} for i in df_fn.columns] if not df_fn.empty else [],
                        style_cell={'textAlign': 'left', 'padding': '10px'},
                        style_header={
                            'backgroundColor': '#e74c3c',
                            'color': 'white',
                            'fontWeight': 'bold'
                        },
                        page_size=10
                    ) if not df_fn.empty else html.P("Aucune donnée disponible")
                ])
            ], className="shadow-sm")
        ])
    ])
], fluid=True)

