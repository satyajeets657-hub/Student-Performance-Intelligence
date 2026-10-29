"""
Student Performance Intelligence System
Main Application Entrypoint
Run directly in VS Code or Terminal using:
    python app.py
"""
import os
import sys
import threading
import time
import webbrowser
from pathlib import Path

# Ensure root directory is on the Python path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from web.app import app, seed_database


def _open_browser():
    time.sleep(1.2)
    try:
        webbrowser.open("http://127.0.0.1:5000")
    except Exception:
        pass


if __name__ == "__main__":
    # Seed the database with records if not already populated
    seed_database()

    # Automatically open browser once the server starts (only on main worker process)
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
        threading.Thread(target=_open_browser, daemon=True).start()

    print("\n" + "=" * 68)
    print("  STUDENT PERFORMANCE INTELLIGENCE SYSTEM IS RUNNING!")
    print("  Website URL   : http://127.0.0.1:5000")
    print("  Teacher Login : teacher / teacher123")
    print("  Student Login : ST0001 / student123")
    print("  Stop Server   : Press Ctrl + C in this terminal")
    print("=" * 68 + "\n")

    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=True)
