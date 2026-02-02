# CardioPredict ML

**Système de prédiction des maladies cardiovasculaires par Machine Learning**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Dash](https://img.shields.io/badge/Dash-2.0+-green.svg)](https://dash.plotly.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-orange.svg)](https://scikit-learn.org/)
[![F1-Score](https://img.shields.io/badge/F1--Score-88.24%25-success.svg)](https://github.com)

## Description

CardioPredict ML est une application web interactive de prédiction des maladies cardiovasculaires développée dans le cadre d'un projet académique. Le système utilise des algorithmes de Machine Learning pour analyser les données cliniques des patients et prédire le risque de maladie cardiaque.

**Objectifs du projet :**
- Analyser et explorer les données médicales cardiovasculaires
- Comparer plusieurs algorithmes de classification
- Développer un outil d'aide à la décision médicale avec une interface utilisateur intuitive
- **Objectif atteint : F1-Score de 88.24% (dépassant l'objectif initial de 85%)**

## Équipe

- **Fatoumata BAH**
- **Poko Ibrahima NOBA**
- **Emmanuel DOSSEKOU**
- **Armand DJEKONBE**

**Superviseur :** Mme Fatou SALL

---

## Structure du projet

```
Projet_ML_classification/
├── Projet_ML_classification.ipynb    # Notebook Jupyter - Pipeline ML complet
├── README.md                          # Documentation du projet
├── X_features.csv                     # Matrice des features (export)
├── y_target.csv                       # Variable cible (export)
│
└── Dashboard/                         # Application web Dash
    ├── app.py                         # Point d'entrée de l'application
    ├── utils.py                       # Fonctions utilitaires
    │
    ├── assets/                        # Fichiers statiques
    │   ├── styles.css                 # Styles CSS personnalisés
    │   ├── landing-animation.css      # Animations page d'accueil
    │   ├── logo.png                   # Logo de l'application
    │   └── ensae_logo.png             # Logo ENSAE
    │
    ├── models/                        # Modèles entraînés
    │   ├── best_model.pkl             # Meilleur modèle (Neural Net optimisé)
    │   ├── neural_net_optimized.pkl   # Neural Network optimisé
    │   ├── naive_bayes_optimized.pkl  # Naive Bayes optimisé
    │   ├── logistic_reg_optimized.pkl # Logistic Regression optimisé
    │   ├── scaler.pkl                 # RobustScaler
    │   └── voting_classifier.pkl      # Classificateur par vote
    │
    ├── data/                          # Données
    │   ├── raw/                       # Données brutes
    │   │   ├── heart_disease_df.csv   # Dataset original (304 lignes)
    │   │   └── heart_disease_df_2.csv # Dataset nettoyé
    │   ├── processed/                 # Données prétraitées
    │   │   ├── X_train_df.csv         # Features d'entraînement
    │   │   └── X_val.csv              # Features de validation
    │   ├── results/                   # Résultats des modèles
    │   │   ├── optimized_df.csv       # Métriques des modèles optimisés
    │   │   ├── cross_validation_results.csv
    │   │   ├── roc_curves_data.json   # Données courbes ROC
    │   │   └── ...
    │   └── history.csv                # Historique des prédictions
    │
    └── pages/                         # Pages du dashboard
        ├── landing.py                 # Page d'accueil
        ├── overview.py                # Vue d'ensemble du projet
        ├── exploration.py             # Exploration des données
        ├── performance.py             # Performance des modèles
        ├── prediction.py              # Prédiction patient
        ├── history.py                 # Historique des prédictions
        ├── documentation.py           # Documentation
        └── errors.py                  # Analyse des faux négatifs
```

---

## Données

### Source
**UCI Heart Disease Dataset** - Jeu de données de référence pour la prédiction des maladies cardiaques.

### Caractéristiques
- **Patients :** 297 (après nettoyage)
- **Features :** 13 indicateurs médicaux
- **Cible :** Présence de maladie cardiaque (binaire)

### Variables

| Variable | Type | Description |
|----------|------|-------------|
| `age` | Numérique | Âge du patient (années) |
| `sex` | Catégorielle | Sexe (0=Femme, 1=Homme) |
| `cp` | Catégorielle | Type de douleur thoracique (1-4) |
| `trestbps` | Numérique | Pression artérielle au repos (mm Hg) |
| `chol` | Numérique | Cholestérol sérique (mg/dl) |
| `fbs` | Catégorielle | Glycémie à jeun > 120 mg/dl (0/1) |
| `restecg` | Catégorielle | Résultats ECG au repos (0-2) |
| `thalach` | Numérique | Fréquence cardiaque maximale (bpm) |
| `exang` | Catégorielle | Angine induite par exercice (0/1) |
| `oldpeak` | Numérique | Dépression ST induite par exercice |
| `slope` | Catégorielle | Pente du segment ST (1-3) |
| `ca` | Numérique | Nombre de vaisseaux majeurs colorés (0-4) |
| `thal` | Catégorielle | Thalassémie (3=Normal, 6=Défaut fixe, 7=Défaut réversible) |

### Qualité des données
- Valeurs manquantes : < 2% (6 lignes supprimées)
- Aucun doublon
- Distribution des classes relativement équilibrée

---

## Modélisation

### Phase 1 : Algorithmes Baseline

Les modèles suivants ont été testés initialement :

| Modèle | Description |
|--------|-------------|
| **Régression Logistique** | Modèle linéaire de base |
| **K-Nearest Neighbors** | Classification par proximité |
| **Support Vector Machine (SVC)** | Séparation par hyperplan |
| **Nu SVC** | Support Vector Classifier avec paramètre nu |
| **Arbre de Décision** | Approche interprétable par arbre |
| **Random Forest** | Ensemble d'arbres de décision |
| **AdaBoost** | Boosting adaptatif |
| **Gradient Boosting** | Boosting par gradient |
| **Naive Bayes** | Approche probabiliste bayésienne |
| **Linear Discriminant Analysis** | Analyse discriminante linéaire |
| **Quadratic Discriminant Analysis** | Analyse discriminante quadratique |
| **Neural Network (MLP)** | Réseau de neurones multicouches |

### Phase 2 : Optimisation Hybride (Top 5)

Les 5 meilleurs modèles ont été sélectionnés selon le F1-Score baseline et optimisés via une **approche hybride RandomSearchCV → GridSearchCV** :

1. **Linear Discriminant Analysis** (F1 baseline: 0.8750)
2. **Naive Bayes** (F1 baseline: 0.8710)
3. **Logistic Regression** (F1 baseline: 0.8615)
4. **Neural Network (MLP)** (F1 baseline: 0.8485)
5. **Support Vectors (SVC)** (F1 baseline: 0.8438)

### Pipeline de prétraitement

1. **Encodage One-Hot** pour les variables catégorielles
2. **RobustScaler** pour les variables numériques (résistant aux outliers)
3. **Alignement des features** pour garantir la cohérence

### Stratégie de validation

- **Split :** 75% entraînement / 25% validation (stratifié)
- **Cross-validation :** 5-Fold Stratifié
- **Optimisation :** 
  - **Phase 1 :** RandomizedSearchCV pour exploration large de l'espace des hyperparamètres
  - **Phase 2 :** GridSearchCV pour affinement autour des meilleurs hyperparamètres trouvés
- **Métrique d'optimisation :** F1-Score (équilibre optimal Precision/Recall)

---

## Résultats

### Top 3 Modèles Optimisés

| Rang | Modèle | Accuracy | Recall | Precision | F1 Score | Amélioration |
|------|--------|----------|--------|-----------|----------|--------------|
| **🥇 1** | **Neural Network (MLP)** | **89.33%** | **90.91%** | **85.71%** | **88.24%** | **+3.99%** ✅ |
| **🥈 2** | **Naive Bayes** | **89.33%** | **81.82%** | **93.10%** | **87.10%** | **0.00%** |
| **🥉 3** | **Logistic Regression** | **88.00%** | **84.85%** | **87.50%** | **86.15%** | **0.00%** |
| 4 | Linear DA | 88.00% | 81.82% | 90.00% | 85.71% | -2.04% |
| 5 | Support Vectors (SVC) | 85.33% | 87.88% | 80.56% | 84.06% | -0.38% |

### Métriques Globales (Top 5)

| Métrique | Valeur | Commentaire |
|----------|--------|-------------|
| **F1-Score Moyen** | **86.25%** | Excellent (>85%) |
| **Recall Moyen** | **85.46%** | Très bon taux de détection |
| **Precision Moyenne** | **87.37%** | Faible taux de faux positifs |
| **Accuracy Moyenne** | **87.87%** | Performance globale excellente |

### Modèle Sélectionné pour Production

**🥇Neural Network (MLP) Optimisé**

**Hyperparamètres optimaux :**
```python
{
    'hidden_layer_sizes': (50, 50, 50),  # Architecture profonde
    'activation': 'logistic',             # Fonction sigmoid
    'alpha': 0.08,                        # Régularisation L2
    'learning_rate': 'constant',
    'learning_rate_init': 0.08,
    'early_stopping': True,
    'max_iter': 1000,
    'random_state': 42
}
```

**Justification du choix :**
- **Meilleur F1-Score** : 88.24% (supérieur à tous les autres modèles)
- **Amélioration significative** : +3.99% par rapport au baseline
- **Excellent Recall** : 90.91% (détection de 91% des cas positifs - crucial en médical)
- **Bonne Precision** : 85.71% (limitation des faux positifs)
- **Meilleure Accuracy** : 89.33%
- **Architecture profonde** : 3 couches cachées capturent mieux les patterns complexes
- **Activation logistic** : Optimale pour ce problème (supérieure à ReLU)

### Insights Clés de l'Optimisation

1. **Architecture Profonde Gagne** : L'architecture (50,50,50) surpasse largement (100,) simple (+3.99%)
2. **Activation Logistic Surprenante** : Sigmoid fonctionne mieux que ReLU pour ce dataset
3. **Importance de la Métrique** : Optimiser F1-Score vs Recall change radicalement les résultats
4. **Simplicité Peut Payer** : Naive Bayes (1 param) arrive 2ème avec 93% de Precision

### Stratégie Multi-Modèles Recommandée

| Contexte | Modèle Recommandé | Raison |
|----------|-------------------|--------|
| **Production principale** | Neural Network (MLP) | Meilleur F1-Score global (88.24%) |
| **Haute Precision requise** | Naive Bayes | 93.10% Precision (minimise faux positifs) |
| **Équilibre parfait** | Logistic Regression | Recall/Precision équilibrés (84.85%/87.50%) |
| **Détection maximale** | SVC | 87.88% Recall (minimise faux négatifs) |

---

## Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Dépendances

```bash
pip install dash
pip install dash-bootstrap-components
pip install pandas
pip install numpy
pip install scikit-learn
pip install plotly
```

Ou créez un fichier `requirements.txt` :

```txt
dash>=2.0.0
dash-bootstrap-components>=1.0.0
pandas>=1.3.0
numpy>=1.21.0
scikit-learn>=1.0.0
plotly>=5.0.0
```

Puis installez avec :

```bash
pip install -r requirements.txt
```

---

## Utilisation

### Lancer l'application

1. Naviguez vers le dossier Dashboard :

```bash
cd Dashboard
```

2. Lancez l'application :

```bash
python app.py
```

3. Ouvrez votre navigateur à l'adresse : `http://localhost:8050`

### Notebook Jupyter

Pour explorer le pipeline ML complet :

```bash
jupyter notebook Projet_ML_classification.ipynb
```

---

## Fonctionnalités du Dashboard

### 1. Page d'accueil
- Présentation visuelle du projet
- Statistiques clés (297 patients, 12 algorithmes testés, 88.24% F1-Score)

### 2. Exploration des données
- 12 KPIs interactifs (démographie, prévalence, etc.)
- Visualisations avec Plotly
- Tests statistiques (chi-carré, distributions)

### 3. Modélisation
- **Phase Baseline** : Comparaison des 12 modèles initiaux
- **Phase Optimisation** : Top 5 modèles avec optimisation hybride
- Métriques détaillées (accuracy, recall, precision, F1, ROC-AUC)
- Classement des top 3 modèles optimisés
- Résultats de validation croisée
- Visualisation des courbes ROC

### 4. Prédiction
- Formulaire interactif pour saisir les données patient
- Prédiction en temps réel avec probabilités (Neural Network optimisé)
- Génération de rapport PDF
- Sauvegarde automatique dans l'historique

### 5. Historique
- Tableau des prédictions passées
- Export CSV
- Suppression de l'historique

---

## Performance et Validation

### Validation Croisée 5-Fold

Le Neural Network optimisé a été validé avec une cross-validation stratifiée 5-fold :

- **F1-Score CV moyen :** 0.8155 ± 0.02
- **F1-Score Validation :** 0.8824
- **Écart CV-Validation :** +0.0669 (généralisation excellente, aucun overfitting)

### Comparaison Avant/Après Optimisation

| Modèle | F1 Baseline | F1 Optimisé | Gain |
|--------|-------------|-------------|------|
| Neural Net | 0.8485 | **0.8824** | **+3.99%** ✅ |
| Naive Bayes | 0.8710 | 0.8710 | 0.00% (stable) |
| Logistic Reg | 0.8615 | 0.8615 | 0.00% (stable) |
| Linear DA | 0.8750 | 0.8571 | -2.04% (acceptable) |
| SVC | 0.8438 | 0.8406 | -0.38% (négligeable) |

### Analyse ROC-AUC

| Modèle | ROC-AUC | Interprétation |
|--------|---------|----------------|
| Neural Network | **0.954** | Excellent |
| Naive Bayes | 0.966 | Excellent |
| Logistic Regression | 0.932 | Excellent |
| Linear DA | 0.945 | Excellent |
| SVC | 0.889 | Très bon |

---

## Avertissement médical

**⚠️ Ce système est un outil d'aide à la décision et ne remplace en aucun cas un diagnostic médical professionnel.**

Les prédictions fournies sont basées sur des modèles statistiques et doivent être interprétées par un professionnel de santé qualifié. Consultez toujours un médecin pour tout problème de santé cardiovasculaire.

**Limitations :**
- Dataset limité à 297 patients
- Modèle entraîné sur des données spécifiques (UCI Heart Disease Dataset)
- Faux négatifs possibles (~9% avec le meilleur modèle)
- Ne prend pas en compte l'historique médical complet du patient

---

## Améliorations Futures

### Court terme
- [ ] Calibration des probabilités avec `CalibratedClassifierCV`
- [ ] Ensemble Learning (VotingClassifier avec les 3 meilleurs modèles)
- [ ] Analyse SHAP pour l'interprétabilité des prédictions

### Moyen terme
- [ ] Feature Engineering avancé (interactions, transformations polynomiales)
- [ ] Nested Cross-Validation pour estimation plus robuste
- [ ] Test sur dataset externe pour validation indépendante

### Long terme
- [ ] Intégration de données temporelles (suivi patient)
- [ ] Modèles de deep learning (CNN, LSTM)
- [ ] Déploiement cloud avec monitoring en production

---

## Contributions

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

---

## Licence

Projet académique - ENSAE - 2026

**Auteurs :**
- Fatoumata BAH
- Poko Ibrahima NOBA
- Emmanuel DOSSEKOU
- Armand DJEKONBE

---

## Références

### Datasets
- [UCI Machine Learning Repository - Heart Disease Dataset](https://archive.ics.uci.edu/ml/datasets/heart+disease)

### Bibliographie
- Dua, D. and Graff, C. (2019). UCI Machine Learning Repository. Irvine, CA: University of California, School of Information and Computer Science.
- Pedregosa et al. (2011). Scikit-learn: Machine Learning in Python. JMLR 12, pp. 2825-2830.
- Plotly Technologies Inc. (2015). Collaborative data science. Montreal, QC.

### Documentation
- [scikit-learn Documentation](https://scikit-learn.org/stable/documentation.html)
- [Dash by Plotly Documentation](https://dash.plotly.com/)
- [MLPClassifier - Neural Networks](https://scikit-learn.org/stable/modules/neural_networks_supervised.html)

---

## Contact

Pour toute question ou suggestion concernant ce projet, veuillez contacter l'équipe via :
- Institution : ENSAE - École Nationale de la Statistique et de l'Analyse Économique

---

**Dernière mise à jour :** Février 2026

**Version :** 2.0 (avec optimisation hybride)

**Status :** Production Ready - F1-Score: 88.24%
