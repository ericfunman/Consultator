"""
Consultator - Plateforme de gestion de consultants
Point d'entrée principal de l'application Streamlit
Optimisé pour gérer 1000+ consultants avec initialisation efficace
"""

import os
import sys

import streamlit as st
from streamlit_option_menu import option_menu

# Ajouter le dossier app au path Python
sys.path.append(os.path.dirname(__file__))

from database.database import init_database

# Configuration de la page
st.set_page_config(
    page_title="Consultator",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS personnalisé optimisé
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
    .stApp > header {
        background-color: transparent;
    }
    .stApp {
        background: linear-gradient(45deg, #f0f4f8, #e8f4fd);
    }
</style>
""",
    unsafe_allow_html=True,
)

@st.cache_resource
def get_navigation_modules():
    """Cache les imports des modules de navigation pour éviter les rechargements"""
    modules = {}
    try:
        from pages_modules import home
        modules['home'] = home
    except Exception as e:
        print(f"Erreur import home: {e}")
    
    try:
        from pages_modules import consultants
        modules['consultants'] = consultants
    except Exception as e:
        print(f"Erreur import consultants: {e}")
    
    try:
        from pages_modules import technologies
        modules['technologies'] = technologies
    except Exception as e:
        print(f"Erreur import technologies: {e}")
    
    try:
        from pages_modules import practices
        modules['practices'] = practices
    except Exception as e:
        print(f"Erreur import practices: {e}")
    
    try:
        from pages_modules import business_managers
        modules['business_managers'] = business_managers
    except Exception as e:
        print(f"Erreur import business_managers: {e}")
    
    try:
        from pages_modules import chatbot
        modules['chatbot'] = chatbot
    except Exception as e:
        print(f"Erreur import chatbot: {e}")
    
    return modules


def main():
    """Fonction principale de l'application optimisée"""

    # Initialiser la base de données UNE SEULE FOIS
    if 'database_initialized' not in st.session_state:
        with st.spinner('🔄 Initialisation de la base de données...'):
            init_database()
            st.session_state.database_initialized = True

    # Header principal
    st.markdown(
        '<div class="main-header">🏢 Consultator</div>', unsafe_allow_html=True
    )
    st.markdown("### 📊 Plateforme de gestion de practice data (1000+ consultants)")

    # Charger les modules avec cache
    modules = get_navigation_modules()

    # Menu de navigation dans la sidebar
    with st.sidebar:
        # Affichage rapide des statistiques si possible
        if 'consultants' in modules:
            try:
                from services.consultant_service import ConsultantService
                stats = ConsultantService.get_consultant_summary_stats()
                st.metric("👥 Total Consultants", stats.get('total_consultants', 0))
                st.metric("✅ Disponibles", stats.get('available_consultants', 0))
                st.divider()
            except:
                pass  # Ignore si erreur stats
        
        selected = option_menu(
            menu_title="🧭 Navigation",
            options=[
                "🏠 Accueil",
                "👥 Consultants",
                "👨‍💼 Business Managers",
                "🏢 Practices",
                "🔧 Technologies",
                "🤖 Assistant IA",
            ],
            icons=["house", "people", "briefcase", "building", "tools", "robot"],
            menu_icon="list",
            default_index=0,
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

    # Navigation vers les pages avec gestion d'erreurs optimisée
    try:
        if selected == "🏠 Accueil":
            if 'home' in modules:
                modules['home'].show()
            else:
                st.error("❌ Module Accueil non disponible")
                
        elif selected == "👥 Consultants":
            if 'consultants' in modules:
                modules['consultants'].show()
            else:
                st.error("❌ Module Consultants non disponible")
                
        elif selected == "👨‍💼 Business Managers":
            if 'business_managers' in modules:
                modules['business_managers'].show()
            else:
                st.error("❌ Module Business Managers non disponible")
                st.info("💡 Vérifiez que le fichier `business_managers.py` existe dans `pages_modules/`")
                
        elif selected == "🏢 Practices":
            if 'practices' in modules:
                modules['practices'].show()
            else:
                st.error("❌ Module Practices non disponible")
                
        elif selected == "🔧 Technologies":
            if 'technologies' in modules:
                modules['technologies'].show()
            else:
                st.error("❌ Module Technologies non disponible")
                
        elif selected == "🤖 Assistant IA":
            if 'chatbot' in modules:
                modules['chatbot'].show()
            else:
                st.error("❌ Module Assistant IA non disponible")
                
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement de la page: {e}")
        import traceback
        with st.expander("🔍 Détails de l'erreur"):
            st.code(traceback.format_exc())


if __name__ == "__main__":
    main()
