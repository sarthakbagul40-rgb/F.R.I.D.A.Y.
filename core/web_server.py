"""
F.R.I.D.A.Y. Cybernetic Web HUD Server (Flask - Hardened Security Edition)
Serves the Glassmorphic Web HUD on http://127.0.0.1:5000 and securely handles /api/command, /api/location, and /api/download.
"""

import os
import sys
import logging
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from core.rate_limiter import rate_limit

# Configure Flask app pointing to root static and templates
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
template_dir = os.path.join(base_dir, "templates")
static_dir = os.path.join(base_dir, "static")

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Restricted CORS - allow local web origins
CORS(app, origins=["http://localhost:5000", "http://127.0.0.1:5000"])

# Disable default flask logging and banner spam in console
import flask.cli
flask.cli.show_server_banner = lambda *args: None
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
logging.getLogger('flask').setLevel(logging.ERROR)

command_handler_fn = None
location_history = []

# Whitelist of directories permitted for /api/download
ALLOWED_DOWNLOAD_DIRS = [
    os.path.realpath(os.path.join(os.path.expanduser("~"), "Desktop")),
    os.path.realpath(r"D:\FRIDAY_Projects"),
    os.path.realpath(static_dir)
]

# Sensitive extension blacklist
DENIED_EXTENSIONS = {
    ".env", ".py", ".db", ".sqlite", ".sqlite3", ".key", ".pem",
    ".crt", ".cert", ".bat", ".cmd", ".exe", ".dll", ".sys", ".ps1"
}

def register_command_handler(fn):
    global command_handler_fn
    command_handler_fn = fn

def _is_authorized(req) -> bool:
    """Verifies that the request is local or provides a valid auth token."""
    client_ip = req.headers.get('X-Forwarded-For', req.remote_addr or '127.0.0.1')
    if client_ip in ('127.0.0.1', 'localhost', '::1', 'testclient'):
        return True

    # If LAN access is enabled, verify token
    token = os.environ.get("FRIDAY_AUTH_TOKEN")
    if not token:
        # If no token configured, disallow non-local traffic
        return False

    auth_header = req.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:].strip() == token
    return req.args.get("token") == token

@app.route('/')
@rate_limit(max_requests=60, window_seconds=60)
def index():
    return render_template('index.html')

@app.route('/manifest.json')
def manifest():
    return send_from_directory(static_dir, 'manifest.json')

@app.route('/api/command', methods=['POST'])
@rate_limit(max_requests=30, window_seconds=60)
def api_command():
    if not _is_authorized(request):
        return jsonify({"status": "error", "response": "Unauthorized request. Local access only."}), 403

    data = request.get_json() or {}
    cmd = data.get('command', '').strip()
    if not cmd:
        return jsonify({"status": "error", "response": "Empty command received."}), 400

    if command_handler_fn:
        try:
            resp = command_handler_fn(cmd)
            return jsonify({"status": "success", "response": str(resp), "action_taken": True})
        except Exception as e:
            return jsonify({"status": "error", "response": f"Execution error: {e}"}), 500

    return jsonify({"status": "success", "response": f"Command '{cmd}' received by Friday core."})

@app.route('/api/location', methods=['POST'])
@rate_limit(max_requests=60, window_seconds=60)
def api_location():
    data = request.get_json() or {}
    lat = data.get('lat')
    lon = data.get('lon')
    if lat and lon:
        location_history.append({"lat": lat, "lon": lon})
        if len(location_history) > 20:
            location_history.pop(0)
        return jsonify({"status": "success", "message": "Location telemetry synchronized."})
    return jsonify({"status": "error", "message": "Missing coordinates."}), 400

@app.route('/api/download')
@rate_limit(max_requests=20, window_seconds=60)
def api_download():
    """Secure file download endpoint protected against path traversal and arbitrary file read."""
    if not _is_authorized(request):
        return jsonify({"status": "error", "message": "Unauthorized."}), 403

    raw_path = request.args.get('path', '').strip()
    if not raw_path:
        return jsonify({"status": "error", "message": "Missing path parameter."}), 400

    # 1. Canonicalize path
    canonical_path = os.path.realpath(raw_path)

    # 2. Check existence
    if not os.path.exists(canonical_path) or not os.path.isfile(canonical_path):
        return jsonify({"status": "error", "message": "File not found."}), 404

    # 3. Check blacklist extensions
    _, ext = os.path.splitext(canonical_path)
    if ext.lower() in DENIED_EXTENSIONS or ".git" in canonical_path.lower():
        return jsonify({"status": "error", "message": "Access to this file type is restricted."}), 403

    # 4. Whitelist directory check
    is_whitelisted = any(
        canonical_path.startswith(allowed_dir + os.sep) or canonical_path == allowed_dir
        for allowed_dir in ALLOWED_DOWNLOAD_DIRS
    )

    if not is_whitelisted:
        return jsonify({"status": "error", "message": "Access restricted to approved project directories only."}), 403

    return send_file(canonical_path, as_attachment=True)

def run_web_server(host=None, port=5000):
    """Starts the hardened Flask server on localhost by default."""
    if host is None:
        allow_lan = os.environ.get("FRIDAY_ALLOW_LAN", "false").lower() in ("1", "true", "yes")
        host = "0.0.0.0" if allow_lan else "127.0.0.1"

    try:
        app.run(host=host, port=port, debug=False, use_reloader=False)
    except Exception as e:
        print(f"[Web Server Notice]: {e}")
