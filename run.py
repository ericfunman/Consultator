"""
Script de lancement de Consultator
Démarre l'application Streamlit
"""

import os
import socket
import subprocess
import sys


def is_port_available(port):
    """Vérifie si un port est disponible"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", port))
            return True
    except OSError:
        return False


def find_available_port(start_port=8501, max_attempts=10):
    """Trouve un port disponible"""
    for port in range(start_port, start_port + max_attempts):
        if is_port_available(port):
            return port
    return None


def run_consultator():
    """Lance l'application Consultator"""

    # Changer vers le répertoire de l'application
    app_dir = os.path.join(os.path.dirname(__file__), "app")

    print("🚀 Lancement de Consultator...")
    print(f"📁 Répertoire: {app_dir}")

    # Trouver un port disponible
    port = find_available_port()
    if port is None:
        print("❌ Aucun port disponible trouvé")
        return

    print(f"🌐 URL: http://localhost:{port}")
    print("⏱️  Démarrage en cours...")

    # Lancer Streamlit
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        os.path.join(app_dir, "main.py"),
        f"--server.port={port}",
        "--server.address=localhost",
        "--browser.gatherUsageStats=false",
    ]

    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Arrêt de Consultator...")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")


if __name__ == "__main__":
    run_consultator()
