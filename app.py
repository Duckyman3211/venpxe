import os
import json
from flask import Flask

app = Flask(__name__, static_folder='static', template_folder='templates')

# Resolve structural asset directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'data', 'config.json')

def init_config():
    """Ensures baseline config matrix structures exist on boot."""
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    if not os.path.exists(CONFIG_PATH):
        baseline = {
            "network": {"interface": "eth0", "server_ip": "192.168.1.10"},
            "timeouts": {"iso_selector_seconds": 5, "script_selector_seconds": 10},
            "profiles": [],
            "hardware_rules": []
        }
        with open(CONFIG_PATH, 'w') as f:
            json.dump(baseline, f, indent=4)

if __name__ == '__main__':
    init_config()
    
    # Import modules to register routes and tasks natively
    from modules.webserver import init_webserver
    from modules.scheduler import start_scheduler
    
    init_webserver(app, CONFIG_PATH)
    start_scheduler(CONFIG_PATH)
    
    print("🌐 VenPXE Core Armed. Control Center listening on http://0.0.0.0:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)