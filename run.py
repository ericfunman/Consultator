"""
Script de lancement de Consultator
Démarre l'application Streamlit
"""

import subprocess
import sys
import os

def run_consultator():
    """Lance l'application Consultator"""
    
    # Changer vers le répertoire de l'application
    app_dir = os.path.join(os.path.dirname(__file__), 'app')
    
    print("🚀 Lancement de Consultator...")
    print(f"📁 Répertoire: {app_dir}")
    print("🌐 URL: http://localhost:8501")
    print("⏱️  Démarrage en cours...")
    
    # Lancer Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run", 
        os.path.join(app_dir, "main.py"),
        "--server.port=8501",
        "--server.address=localhost",
        "--browser.gatherUsageStats=false"
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Arrêt de Consultator...")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")

if __name__ == "__main__":
    run_consultator()
