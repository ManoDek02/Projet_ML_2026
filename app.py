"""
Point d'entrée pour le déploiement Render
Configure les chemins Python et importe l'application Dash
"""
import sys
import os

# Obtenir le répertoire de base du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ajouter Dashboard au Python path
dashboard_dir = os.path.join(BASE_DIR, 'Dashboard')
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

# Ajouter aussi le répertoire racine
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Maintenant on peut importer l'app
# Note: on importe depuis Dashboard.app car c'est là que se trouve le fichier
import Dashboard.app as dash_app

# Exporte les objets nécessaires pour gunicorn
app = dash_app.app
server = dash_app.server

# Pour l'exécution locale
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(host='0.0.0.0', port=port, debug=False)
```

### 🔧 Change la Start Command dans Render

Va dans les Settings de Render et change la **Start Command** vers :
```
gunicorn app:server
