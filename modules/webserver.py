# modules/webserver.py
import os
import json
from flask import render_template, request, redirect, jsonify

# Directory targets based on your project layout
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ISO_DIR = os.path.join(BASE_DIR, 'iso')
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts')

def load_db(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def save_db(config_path, data):
    with open(config_path, 'w') as f:
        json.dump(data, f, indent=4)

def scan_allowed_assets():
    """Scans storage directories to populate UI dropdown choices dynamically."""
    isos = []
    if os.path.exists(ISO_DIR):
        for f in os.listdir(ISO_DIR):
            if f.endswith('.iso'):
                size_gb = round(os.path.getsize(os.path.join(ISO_DIR, f)) / (1024**3), 1)
                isos.append({"filename": f, "size": f"{size_gb} GB"})
                
    scripts = ["none"]
    if os.path.exists(SCRIPTS_DIR):
        for root, _, files in os.walk(SCRIPTS_DIR):
            for f in files:
                if f.endswith(('.xml', '.cfg', '.ini', 'cloud-init-user-data')):
                    # Create a relative path from the scripts root (e.g., "example/autounattend.xml")
                    rel_path = os.path.relpath(os.path.join(root, f), SCRIPTS_DIR)
                    scripts.append(rel_path)
                    
    return isos, scripts

def init_webserver(app, config_path):
    """Hooks all dynamic page views and API targets into app.py."""
    
    @app.route('/')
    @app.route('/index.html')
    def index():
        # Active sessions will eventually hook into scheduler tracking data
        return render_template('index.html')

    @app.route('/configurations.html', methods=['GET', 'POST'])
    def configurations():
        db = load_db(config_path)
        if request.method == 'POST':
            db['network']['interface'] = request.form.get('adapter')
            db['network']['server_ip'] = request.form.get('server_ip')
            db['timeouts']['iso_selector_seconds'] = int(request.form.get('iso_timeout', 5))
            db['timeouts']['script_selector_seconds'] = int(request.form.get('script_timeout', 10))
            save_db(config_path, db)
            return redirect('/configurations.html')
            
        return render_template('configurations.html', config=db)

    @app.route('/management.html')
    def management():
        db = load_db(config_path)
        isos, scripts = scan_allowed_assets()
        return render_template('management.html', isos=isos, scripts=scripts, profiles=db.get('profiles', []))

    @app.route('/filters.html', methods=['GET', 'POST'])
    def filters():
        db = load_db(config_path)
        isos, scripts = scan_allowed_assets()
        
        if request.method == 'POST':
            # Handle creating a new automated filter binding rule
            mac = request.form.get('mac_address', '').strip().upper()
            selected_iso = request.form.get('iso')
            selected_script = request.form.get('script')
            
            if mac:
                # Remove existing rule for this MAC if it exists to avoid duplicates
                db['hardware_rules'] = [r for r in db['hardware_rules'] if r['mac_address'] != mac]
                db['hardware_rules'].append({
                    "mac_address": mac,
                    "iso": selected_iso,
                    "script": selected_script
                })
                save_db(config_path, db)
            return redirect('/filters.html')

        return render_template('filters.html', rules=db.get('hardware_rules', []), isos=isos, scripts=scripts)

    @app.route('/api/filters/delete/<mac>', methods=['POST'])
    def delete_filter(mac):
        db = load_db(config_path)
        db['hardware_rules'] = [r for r in db['hardware_rules'] if r['mac_address'] != mac.upper()]
        save_db(config_path, db)
        return jsonify({"status": "success"})

    @app.route('/info.html')
    def info():
        return render_template('info.html')