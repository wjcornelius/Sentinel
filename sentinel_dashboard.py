# -*- coding: utf-8 -*-
"""
Sentinel Dashboard - Web Interface

Flask-based dashboard for controlling and monitoring Sentinel.
Provides live terminal streaming, config toggles, and approval UI.
"""

from flask import Flask, render_template, request, jsonify, Response
import subprocess
import threading
import time
import os
import sys
import json
import logging as flask_logging
from datetime import datetime
import config

# Setup Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sentinel-nautical-dashboard-2025'

# Global state
current_process = None
process_lock = threading.Lock()
terminal_buffer = []
current_status = "idle"  # idle, running, waiting_approval, waiting_plan_decision, completed, aborted, failed
current_plan = None


@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('dashboard.html',
                         live_trading=config.LIVE_TRADING,
                         dev_reruns=getattr(config, 'ALLOW_DEV_RERUNS', False))


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration."""
    return jsonify({
        'LIVE_TRADING': config.LIVE_TRADING,
        'ALLOW_DEV_RERUNS': getattr(config, 'ALLOW_DEV_RERUNS', False)
    })


@app.route('/api/start', methods=['POST'])
def start_sentinel():
    """Start Sentinel run with provided configuration."""
    global current_process, current_status, terminal_buffer, current_plan

    with process_lock:
        if current_process and current_process.poll() is None:
            return jsonify({'error': 'Sentinel is already running'}), 400

        # Get config from request
        data = request.json or {}
        live_trading = data.get('LIVE_TRADING', False)
        dev_reruns = data.get('ALLOW_DEV_RERUNS', False)

        # Update config.py
        try:
            update_config(live_trading, dev_reruns)
        except Exception as e:
            return jsonify({'error': f'Failed to update config: {str(e)}'}), 500

        # Clear state
        terminal_buffer = []
        current_status = "running"
        current_plan = None

        # Start Sentinel in background thread
        thread = threading.Thread(target=run_sentinel_process, daemon=True)
        thread.start()

        return jsonify({
            'status': 'started',
            'config': {
                'LIVE_TRADING': live_trading,
                'ALLOW_DEV_RERUNS': dev_reruns
            }
        })


@app.route('/api/stop', methods=['POST'])
def stop_sentinel():
    """Request graceful abort of running Sentinel."""
    global current_process, current_status

    with process_lock:
        if not current_process or current_process.poll() is not None:
            return jsonify({'error': 'Sentinel is not running'}), 400

        # Send abort signal via UI bridge
        from sentinel.ui_bridge import request_abort
        request_abort()

        current_status = "aborting"
        add_terminal_output("\n[DASHBOARD] Abort requested - waiting for safe stop point...\n")

        return jsonify({'status': 'abort_requested'})


@app.route('/api/approve', methods=['POST'])
def approve_plan():
    """Approve trade plan."""
    global current_status

    if current_status != "waiting_approval":
        return jsonify({'error': 'Not waiting for approval'}), 400

    from sentinel.ui_bridge import set_approval_response
    set_approval_response(True)

    add_terminal_output("\n[DASHBOARD] Trade plan APPROVED by user\n")
    current_status = "running"

    return jsonify({'status': 'approved'})


@app.route('/api/deny', methods=['POST'])
def deny_plan():
    """Deny trade plan."""
    global current_status

    if current_status != "waiting_approval":
        return jsonify({'error': 'Not waiting for approval'}), 400

    from sentinel.ui_bridge import set_approval_response
    set_approval_response(False)

    add_terminal_output("\n[DASHBOARD] Trade plan DENIED by user\n")
    current_status = "completed"

    return jsonify({'status': 'denied'})


@app.route('/api/reuse_plan', methods=['POST'])
def reuse_plan():
    """Reuse existing plan."""
    global current_status

    if current_status != "waiting_plan_decision":
        return jsonify({'error': 'Not waiting for plan decision'}), 400

    from sentinel.ui_bridge import set_plan_regeneration_response
    set_plan_regeneration_response(False)

    add_terminal_output("\n[DASHBOARD] User chose to REUSE existing plan\n")
    current_status = "running"

    return jsonify({'status': 'reusing'})


@app.route('/api/regenerate_plan', methods=['POST'])
def regenerate_plan():
    """Regenerate plan from scratch."""
    global current_status

    if current_status != "waiting_plan_decision":
        return jsonify({'error': 'Not waiting for plan decision'}), 400

    from sentinel.ui_bridge import set_plan_regeneration_response
    set_plan_regeneration_response(True)

    add_terminal_output("\n[DASHBOARD] User chose to REGENERATE plan\n")
    current_status = "running"

    return jsonify({'status': 'regenerating'})


@app.route('/api/status')
def get_status():
    """Get current status and terminal output."""
    global terminal_buffer, current_status, current_plan

    return jsonify({
        'status': current_status,
        'terminal': terminal_buffer[-100:],  # Last 100 lines
        'plan': current_plan
    })


@app.route('/api/stream')
def stream():
    """Server-sent events stream for real-time terminal output."""
    def generate():
        last_size = 0
        while True:
            # Send new terminal lines
            if len(terminal_buffer) > last_size:
                for line in terminal_buffer[last_size:]:
                    yield f"data: {json.dumps({'type': 'terminal', 'data': line})}\n\n"
                last_size = len(terminal_buffer)

            # Send status updates
            yield f"data: {json.dumps({'type': 'status', 'status': current_status})}\n\n"

            time.sleep(0.5)  # Update every 500ms

    return Response(generate(), mimetype='text/event-stream')


def update_config(live_trading, dev_reruns):
    """Update config.py with new values."""
    # Read current config
    with open('config.py', 'r') as f:
        lines = f.readlines()

    # Update values
    new_lines = []
    for line in lines:
        if line.strip().startswith('LIVE_TRADING'):
            new_lines.append(f'LIVE_TRADING = {live_trading}\n')
        elif line.strip().startswith('ALLOW_DEV_RERUNS'):
            new_lines.append(f'ALLOW_DEV_RERUNS = {dev_reruns}\n')
        else:
            new_lines.append(line)

    # Write updated config
    with open('config.py', 'w') as f:
        f.writelines(new_lines)

    # Reload config module
    import importlib
    importlib.reload(config)


def add_terminal_output(text):
    """Add text to terminal buffer."""
    global terminal_buffer
    terminal_buffer.append(text)


def run_sentinel_process():
    """Run main_script.py and capture output."""
    global current_process, current_status, terminal_buffer

    try:
        # Set environment variable for UI mode
        env = os.environ.copy()
        env['SENTINEL_UI_MODE'] = '1'

        # Use venv Python if available, otherwise system Python
        venv_python = os.path.join('venv', 'Scripts', 'python.exe')
        python_executable = venv_python if os.path.exists(venv_python) else sys.executable

        # Start process
        current_process = subprocess.Popen(
            [python_executable, 'main_script.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=env
        )

        # Stream output
        for line in iter(current_process.stdout.readline, ''):
            if line:
                add_terminal_output(line)

                # Check for special events
                if 'Manual Approval Required' in line:
                    current_status = "waiting_approval"
                elif 'Existing plan detected' in line or 'Waiting for plan decision' in line:
                    current_status = "waiting_plan_decision"
                elif 'ABORTED' in line:
                    current_status = "aborted"

        # Wait for completion
        current_process.wait()

        if current_status not in ["aborted", "waiting_approval"]:
            if current_process.returncode == 0:
                current_status = "completed"
                add_terminal_output("\n[DASHBOARD] Sentinel run completed successfully\n")
            else:
                current_status = "failed"
                add_terminal_output(f"\n[DASHBOARD] Sentinel run failed with code {current_process.returncode}\n")

    except Exception as e:
        current_status = "failed"
        add_terminal_output(f"\n[DASHBOARD] Error: {str(e)}\n")
        flask_logging.error(f"Process error: {e}", exc_info=True)


if __name__ == '__main__':
    print("=" * 60)
    print("SENTINEL DASHBOARD")
    print("=" * 60)
    print("\nStarting dashboard server...")
    print("Open your browser to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)

    app.run(debug=False, host='0.0.0.0', port=5000)
