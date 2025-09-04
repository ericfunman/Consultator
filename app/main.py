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
        font-size: 3.5rem;
        font-weight: 900;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 3rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #1f77b4, #2196F3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        letter-spacing: 2px;
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

def get_navigation_modules():
    """Charge les modules de navigation sans cache pour éviter les problèmes"""
    modules = {}
    
    # Module home
    try:
        import importlib
        import pages_modules.home as home_module
        importlib.reload(home_module)
        modules['home'] = home_module
        print("✅ Module home chargé avec succès")
    except Exception as e:
        print(f"❌ Erreur import home: {e}")
        modules['home'] = None
    
    # Module consultants
    try:
        import pages_modules.consultants as consultants_module
        importlib.reload(consultants_module)
        modules['consultants'] = consultants_module
        print("✅ Module consultants chargé avec succès")
    except Exception as e:
        print(f"❌ Erreur import consultants: {e}")
        # Essayer consultant_profile en fallback
        try:
            import pages_modules.consultant_profile as consultant_profile_module
            importlib.reload(consultant_profile_module)
            modules['consultants'] = consultant_profile_module
            print("✅ Module consultant_profile chargé comme fallback")
        except Exception as e2:
            print(f"❌ Erreur import consultant_profile: {e2}")
            modules['consultants'] = None
    
    # Module technologies
    try:
        import pages_modules.technologies as technologies_module
        importlib.reload(technologies_module)
        modules['technologies'] = technologies_module
        print("✅ Module technologies chargé avec succès")
    except Exception as e:
        print(f"❌ Erreur import technologies: {e}")
        modules['technologies'] = None
    
    # Module practices
    try:
        import pages_modules.practices as practices_module
        importlib.reload(practices_module)
        modules['practices'] = practices_module
        print("✅ Module practices chargé avec succès")
    except Exception as e:
        print(f"❌ Erreur import practices: {e}")
        modules['practices'] = None
    
    # Module business_managers
    try:
        import pages_modules.business_managers as business_managers_module
        importlib.reload(business_managers_module)
        modules['business_managers'] = business_managers_module
        print("✅ Module business_managers chargé avec succès")
    except Exception as e:
        print(f"❌ Erreur import business_managers: {e}")
        modules['business_managers'] = None
    
    # Module chatbot
    try:
        import pages_modules.chatbot as chatbot_module
        importlib.reload(chatbot_module)
        modules['chatbot'] = chatbot_module
        print("✅ Module chatbot chargé avec succès")
    except Exception as e:
        print(f"❌ Erreur import chatbot: {e}")
        modules['chatbot'] = None
    
    return modules


def show_fallback_home():
    """Page d'accueil de fallback si le module home ne charge pas"""
    st.title("🏠 Tableau de bord")
    st.markdown("### Vue d'ensemble de votre practice data")
    
    # Métriques de base
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("👥 Consultants", "60", "Actifs dans la practice")
    
    with col2:
        st.metric("💼 Missions", "45", "En cours et terminées")
    
    with col3:
        st.metric("📊 Taux d'occupation", "85%", "2%")
    
    st.markdown("---")
    st.info("⚠️ Page d'accueil en mode simplifié - Certaines fonctionnalités peuvent être limitées")


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

    # Charger les modules avec cache
    modules = get_navigation_modules()

    # Menu de navigation dans la sidebar
    with st.sidebar:
        selected = option_menu(
            menu_title=None,
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
            if 'home' in modules and modules['home'] is not None:
                modules['home'].show()
            else:
                st.error("❌ Module Accueil non disponible")
                show_fallback_home()
                
        elif selected == "👥 Consultants":
            if 'consultants' in modules and modules['consultants'] is not None:
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
