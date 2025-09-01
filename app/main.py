"""
Consultator - Plateforme de gestion de consultants
Point d'entrée principal de l'application Streamlit
"""

import os
import sys

import streamlit as st
from streamlit_option_menu import option_menu

# Ajouter le dossier app au path Python
sys.path.append(os.path.dirname(__file__))

from database.database import init_database

# Import des pages
from pages_modules import consultants
from pages_modules import home
from pages_modules import technologies
from pages_modules import practices
# Import business_managers fait dynamiquement pour éviter les erreurs de chargement
from pages_modules import chatbot

# Configuration de la page
st.set_page_config(
    page_title="Consultator",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS personnalisé
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)


def main():
    """Fonction principale de l'application"""

    # Initialiser la base de données
    init_database()

    # Header principal
    st.markdown(
        '<div class="main-header"> Consultator</div>', unsafe_allow_html=True
    )
    st.markdown("### Plateforme de gestion de practice data")

    # Menu de navigation dans la sidebar
    with st.sidebar:
        selected = option_menu(
            menu_title=None,  # Pas de titre
            options=[
                "🏠 Accueil",
                "👥 Consultants",
                "👨‍💼 Business Managers",
                "🏢 Practices",
                "🔧 Référentiel Technologies",
                "🤖 Assistant IA",
            ],
            icons=["house", "people", "briefcase", "building", "tools", "robot"],
            menu_icon="list",
            default_index=0,  # Démarre sur Accueil au lieu de Consultants
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "#fafafa",
                },
                "icon": {"color": "#1f77b4", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#1f77b4"},
            },
        )

    # Navigation vers les pages
    if selected == "🏠 Accueil":
        home.show()
    elif selected == "👥 Consultants":
        consultants.show()
    elif selected == "👨‍💼 Business Managers":
        try:
            from pages_modules import business_managers
            business_managers.show()
        except Exception as e:
            st.error("🚫 Erreur lors du chargement du module Business Managers")
            st.error(f"Détails: {e}")
            import traceback
            st.code(traceback.format_exc())
    elif selected == "🏢 Practices":
        practices.show()
    elif selected == "🔧 Référentiel Technologies":
        technologies.show()
    elif selected == "🤖 Assistant IA":
        chatbot.show()


if __name__ == "__main__":
    main()
