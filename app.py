import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dashboard_dir = os.path.join(BASE_DIR, 'Dashboard')
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import Dashboard.app as dash_app

app = dash_app.app
server = dash_app.server

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(host='0.0.0.0', port=port, debug=False)
