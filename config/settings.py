"""
Configuration de l'application Consultator
Paramètres et constantes globales
"""

import os
from pathlib import Path

# Chemins de base
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"

# Configuration de la base de données
DATABASE_NAME = "consultator.db"
DATABASE_PATH = DATA_DIR / DATABASE_NAME

# Configuration Streamlit
STREAMLIT_CONFIG = {
    "page_title": "Consultator",
    "page_icon": "👥",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Configuration de l'application
APP_CONFIG = {
    "app_name": "Consultator",
    "version": "1.0.0",
    "description": "Plateforme de gestion de practice data",
    "author": "Équipe Consultator",
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "supported_cv_formats": [".pdf", ".docx", ".doc"]
}

# Paramètres de pagination
PAGINATION = {
    "consultants_per_page": 20,
    "missions_per_page": 15,
    "max_search_results": 100
}

# Messages de l'application
MESSAGES = {
    "database_init_success": "✅ Base de données initialisée avec succès !",
    "database_init_error": "❌ Erreur lors de l'initialisation de la base de données",
    "consultant_added": "✅ Consultant ajouté avec succès !",
    "consultant_updated": "✅ Consultant mis à jour avec succès !",
    "consultant_deleted": "✅ Consultant supprimé avec succès !",
    "file_upload_success": "📄 Fichier uploadé avec succès !",
    "file_upload_error": "❌ Erreur lors de l'upload du fichier",
    "cv_parsing_success": "🎯 CV analysé avec succès !",
    "cv_parsing_error": "❌ Erreur lors de l'analyse du CV"
}

# Styles CSS personnalisés
CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .success-box {
        padding: 20px;
        border: 2px solid #2ca02c;
        border-radius: 10px;
        background-color: #f0fff0;
        text-align: center;
    }
    
    .warning-box {
        padding: 20px;
        border: 2px solid #ff7f0e;
        border-radius: 10px;
        background-color: #fff8e1;
        text-align: center;
    }
    
    .info-box {
        padding: 20px;
        border: 2px solid #1f77b4;
        border-radius: 10px;
        background-color: #e3f2fd;
        text-align: center;
    }
</style>
"""

def create_directories():
    """Crée les répertoires nécessaires s'ils n'existent pas"""
    directories = [DATA_DIR, UPLOADS_DIR]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def get_app_info():
    """Retourne les informations de l'application"""
    return {
        "name": APP_CONFIG["app_name"],
        "version": APP_CONFIG["version"],
        "description": APP_CONFIG["description"],
        "database_path": str(DATABASE_PATH),
        "uploads_path": str(UPLOADS_DIR)
    }
