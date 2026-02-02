
"""
Sauvegardez ce contenu dans: utils.py
"""

import pandas as pd
import numpy as np
import pickle
import json
import os
from pathlib import Path
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import html

# ============================================================================
# CHARGEMENT DES DONNÉES
# ============================================================================

def load_model(model_path='models/best_model.pkl'):
    """Charge le modèle sauvegardé avec chemin absolu"""
    try:
        # Si le chemin est relatif, le convertir en absolu
        if not os.path.isabs(model_path):
            # Obtenir le chemin du fichier actuel (utils.py)
            current_file = os.path.abspath(__file__)
            # Remonter au dossier racine du projet
            base_dir = os.path.dirname(os.path.dirname(current_file))
            # Construire le chemin absolu
            model_path = os.path.join(base_dir, model_path)
        
        print(f"Chargement du modèle depuis: {model_path}")
        
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            print(f"✓ Modèle chargé avec succès")
            return model
        else:
            print(f"Fichier modèle non trouvé: {model_path}")
            return None
    except Exception as e:
        print(f"Erreur chargement modèle: {e}")
        return None


def load_scaler(scaler_path='models/scaler.pkl'):
    """Charge le scaler avec chemin absolu"""
    try:
        # Si le chemin est relatif, le convertir en absolu
        if not os.path.isabs(scaler_path):
            # Obtenir le chemin du fichier actuel (utils.py)
            current_file = os.path.abspath(__file__)
            # Remonter au dossier racine du projet
            base_dir = os.path.dirname(os.path.dirname(current_file))
            # Construire le chemin absolu
            scaler_path = os.path.join(base_dir, scaler_path)
        
        print(f"Chargement du scaler depuis: {scaler_path}")
        
        if os.path.exists(scaler_path):
            with open(scaler_path, 'rb') as f:
                scaler = pickle.load(f)
            print(f"✓ Scaler chargé avec succès")
            return scaler
        else:
            print(f"Fichier scaler non trouvé: {scaler_path}")
            return None
    except Exception as e:
        print(f"Erreur chargement scaler: {e}")
        return None

def load_data():
    """Charge un fichier CSV"""
    current_file = os.path.abspath(__file__)
    dashboard_dir = os.path.dirname(current_file)  # Reste dans Dashboard/    
    data_path = os.path.join(dashboard_dir, 'data', 'results', 'heart_disease_df_3.csv')
    df = pd.read_csv(data_path)
    return df

def load_data_2():
    """Charge un fichier CSV"""
    current_file = os.path.abspath(__file__)
    dashboard_dir = os.path.dirname(current_file)  # Reste dans Dashboard/    
    data_path = os.path.join(dashboard_dir, 'data', 'raw', 'heart_disease_df_2.csv')
    df = pd.read_csv(data_path)
    return df

def load_optimized_models():
    """Charge les résultats optimisés et retourne un dict formaté"""
    current_file = os.path.abspath(__file__)
    dashboard_dir = os.path.dirname(current_file)  # Reste dans Dashboard/
    data_path = os.path.join(dashboard_dir, 'data', 'results', 'optimized_df.csv')
    df = pd.read_csv(data_path)
    df = df.set_index('Modèle')

    # Renommer les colonnes en minuscules
    df = df.rename(columns={
        'Accuracy': 'accuracy',
        'Recall': 'recall',
        'Precision': 'precision',
        'F1': 'f1_score',
        'ROC-AUC': 'roc_auc',
        'FN': 'fn',
        'FP': 'fp',
        'TP': 'tp',
        'TN': 'tn'
    })

    # Convertir les pourcentages en décimales
    for col in ['accuracy', 'recall', 'precision', 'f1_score']:
        df[col] = df[col] / 100

    results = {}
    for model_name, row in df.iterrows():
        if model_name == 'Neural Net':
            model_name = 'Neural Network'

        # Reconstruire la matrice de confusion
        cm = np.array([[row['tn'], row['fp']], [row['fn'], row['tp']]])

        results[model_name] = {
            'accuracy': row['accuracy'],
            'precision': row['precision'],
            'recall': row['recall'],
            'f1_score': row['f1_score'],
            'cv_mean': 0,  # Non disponible
            'cv_std': 0,
            'y_pred': None,  # Non disponible
            'y_pred_proba': None,
            'confusion_matrix': cm
        }

    # Métadonnées minimales
    results['_metadata'] = {
        'y_test': None  # Non disponible
    }

    return results


def load_metrics():
    """Charge toutes les métriques depuis les fichiers"""
    try:
        
        # Courbes ROC
        current_file = os.path.abspath(__file__)
        dashboard_dir = os.path.dirname(current_file)  # Reste dans Dashboard/
        
        metrics_path = os.path.join(dashboard_dir, 'data', 'results', 'roc_curves_data.json')
        if os.path.exists(metrics_path):
            with open(metrics_path, 'r') as f:
                return json.load(f)
            roc_data = json.load(f)
        else:
            print("Fichier métriques non trouvé")
            return {}
        
        # Validation croisée
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, 'data', 'results', 'cross_validation_results.csv')
        df_cv = pd.read_csv(data_path)
        
        return {
            'roc': roc_data,
            'cv': df_cv,
        }
    except Exception as e:
        print(f"Erreur chargement métriques: {e}")
        return None


# Ajouter ces lignes :
VARS_NUM = [
    'âge', 'cholestérol', 'pression_artérielle_repos',
    'fréquence_cardiaque_maximale', 'dépression_st',
    'nombre_vaisseaux_majeurs'
]

COLORS = {
    'primary': '#3498db',
    'success': '#27ae60',
    'danger': '#e74c3c',
    'warning': '#f39c12',
    'info': '#17a2b8',
    'dark': '#2c3e50',
    'light': '#ecf0f1',
    'background': '#f8f9fa'
}

def make_prediction(model, scaler, patient_df):
    """
    Applique le même preprocessing que pendant l'entraînement
    """

    try:
        df = patient_df.copy()

        # ================================
        # 1. ONE-HOT ENCODING MANUEL
        # ================================

        df_encoded = pd.DataFrame()

        # Sexe
        df_encoded['sexe_homme'] = (df['sexe'] == 1).astype(int)

        # Glycémie à jeun
        df_encoded['glycémie_à_jeun_supérieure à 120mg/ml'] = (df['glycémie_à_jeun'] == 1).astype(int)

        # Angine exercice
        df_encoded['angine_induite_par_exercice_oui'] = (df['angine_induite_par_exercice'] == 1).astype(int)

        # Pente ST
        df_encoded['pente_st_plate'] = (df['pente_st'] == 2).astype(int)
        df_encoded['pente_st_descendante'] = (df['pente_st'] == 3).astype(int)

        # ================================
        # 2. VARIABLES NUMÉRIQUES
        # ================================

        df_encoded['âge'] = df['âge']
        df_encoded['cholestérol'] = df['cholestérol']
        df_encoded['pression_artérielle_repos'] = df['pression_artérielle_repos']
        df_encoded['fréquence_cardiaque_maximale'] = df['fréquence_cardiaque_maximale']
        df_encoded['dépression_st'] = df['dépression_st']
        df_encoded['nombre_vaisseaux_majeurs'] = df['nombre_vaisseaux_majeurs']

        # ================================
        # 3. ALIGNEMENT DES FEATURES
        # ================================

        expected_features = model.feature_names_in_

        for col in expected_features:
            if col not in df_encoded.columns:
                df_encoded[col] = 0

        df_encoded = df_encoded[expected_features]

        # ================================
        # 4. SCALING
        # ================================

        num_cols = [
            'âge', 'cholestérol', 'pression_artérielle_repos',
            'fréquence_cardiaque_maximale', 'dépression_st',
            'nombre_vaisseaux_majeurs'
        ]

        df_encoded[num_cols] = scaler.transform(df_encoded[num_cols])

        # ================================
        # 5. PRÉDICTION
        # ================================

        prediction = model.predict(df_encoded)[0]
        probas = model.predict_proba(df_encoded)[0]

        return prediction, probas, None

    except Exception as e:
        return None, None, str(e)



# ============================================================================
# MAPPINGS
# ============================================================================

FEATURE_LABELS = {
    'age': 'Âge',
    'sex': 'Sexe',
    'cp': 'Type de douleur thoracique',
    'trestbps': 'Pression artérielle au repos',
    'chol': 'Cholestérol sérique',
    'fbs': 'Glycémie à jeun > 120 mg/dl',
    'restecg': 'Résultats ECG au repos',
    'thalach': 'Fréquence cardiaque maximale',
    'exang': 'Angine induite par exercice',
    'oldpeak': 'Dépression ST',
    'slope': 'Pente du segment ST',
    'ca': 'Nombre de vaisseaux majeurs',
    'thal': 'Thalassémie'
}

FEATURE_MAPPINGS = {
    'sex': {0: 'Femme', 1: 'Homme'},
    'cp': {1: 'Angine Typique', 2: 'Angine Atypique', 3: 'Douleur Non-Angineuse', 4: 'Asymptomatique'},
    'fbs': {0: 'Non', 1: 'Oui'},
    'restecg': {0: 'Normal', 1: 'Anomalie ST-T', 2: 'Hypertrophie VG'},
    'exang': {0: 'Non', 1: 'Oui'},
    'slope': {1: 'Ascendante', 2: 'Plate', 3: 'Descendante'},
    'thal': {3: 'Normal', 6: 'Défaut Fixe', 7: 'Défaut Réversible'}
}
