import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table, callback, Input, Output, no_update
import pandas as pd
import os
import datetime

dash.register_page(__name__, path='/history', name='Historique', title='Historique des Prédictions', description='Consultez l\'historique des prédictions effectuées.')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_PATH = os.path.join(BASE_DIR, "data", "history.csv")

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.H2("Historique des Prédictions", className="mb-0 text-primary"), width="auto"),
                dbc.Col(
                    [
                        dbc.Button([
                            html.I(className="fas fa-download me-2"),
                            "Exporter CSV"
                        ], id="btn-export-csv", color="success", size="sm", className="me-2"),
                        dcc.ConfirmDialogProvider(
                            children=dbc.Button([
                                html.I(className="fas fa-trash me-2"),
                                "Supprimer Historique"
                            ], color="danger", size="sm"),
                            id="confirm-delete",
                            message="Voulez-vous vraiment supprimer tout l'historique ?"
                        ),
                        dcc.Download(id="download-history-csv"),
                    ],
                    width="auto",
                    className="d-flex align-items-center"
                )
            ],
            className="mb-4 align-items-center"
        ),
        
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(id="history-table-container"),
                    dcc.Interval(id="history-interval", interval=5000, n_intervals=0), # Refresh every 5s
                    html.Div(id="delete-output", style={"display": "none"})
                ]
            ),
            className="medical-card"
        )
    ],
    fluid=True
)

@callback(
    Output("history-table-container", "children"),
    Input("history-interval", "n_intervals")
)
def update_history(n):
    if not os.path.exists(HISTORY_PATH):
        return dbc.Alert("Aucun historique disponible.", color="info")
        
    try:
        df = pd.read_csv(HISTORY_PATH)
        # Sort by date descending if 'date' column exists
        if 'date' in df.columns:
            df = df.sort_values(by='date', ascending=False)
            
        return dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold', 'color': '#0d6efd'},
            style_data_conditional=[
                {
                    'if': {'filter_query': '{prediction} = 1'},
                    'backgroundColor': '#fff3cd',
                    'color': '#856404'
                }
            ]
        )
    except Exception as e:
        return dbc.Alert(f"Erreur de lecture de l'historique : {e}", color="danger")

@callback(
    Output("delete-output", "children"),
    Input("confirm-delete", "submit_n_clicks"),
    prevent_initial_call=True
)
def delete_history(n):
    if n:
        if os.path.exists(HISTORY_PATH):
            os.remove(HISTORY_PATH)
    return ""

@callback(
    Output("download-history-csv", "data"),
    Input("btn-export-csv", "n_clicks"),
    prevent_initial_call=True
)
def export_history_csv(n_clicks):
    """Exporte l'historique des prédictions en CSV"""
    if not n_clicks:
        return no_update
    
    if not os.path.exists(HISTORY_PATH):
        return no_update
    
    try:
        df = pd.read_csv(HISTORY_PATH)
        # Trier par date si la colonne existe
        if 'date' in df.columns:
            df = df.sort_values(by='date', ascending=False)
        
        # Générer un nom de fichier avec la date actuelle
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"historique_predictions_{timestamp}.csv"
        
        return dcc.send_data_frame(df.to_csv, filename, index=False)
    except Exception as e:
        print(f"Erreur lors de l'exportation: {e}")
        return no_update