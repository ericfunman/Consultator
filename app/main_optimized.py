"""
Consultator - Version optimisée pour démarrage rapide
Chargement lazy des modules et cache intelligent
"""

import os
import sys

import streamlit as st
from streamlit_option_menu import option_menu

# Ajouter le dossier app au path Python
sys.path.append(os.path.dirname(__file__))

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


def load_module_lazy(module_name):
    """Charge un module de façon lazy avec cache"""
    cache_key = f"module_{module_name}"

    if cache_key not in st.session_state:
        try:
            if module_name == 'home':
                import pages_modules.home as module
            elif module_name == 'consultants':
                import pages_modules.consultants as module
            elif module_name == 'technologies':
                import pages_modules.technologies as module
            elif module_name == 'practices':
                import pages_modules.practices as module
            elif module_name == 'business_managers':
                import pages_modules.business_managers as module
            elif module_name == 'chatbot':
                import pages_modules.chatbot as module
            else:
                return None

            st.session_state[cache_key] = module
            print(f"✅ Module {module_name} chargé et mis en cache")

        except Exception as e:
            print(f"❌ Erreur import {module_name}: {e}")
            st.session_state[cache_key] = None

    return st.session_state[cache_key]


def init_database_fast():
    """Initialisation rapide de la base de données avec cache"""
    if 'database_ready' not in st.session_state:
        with st.spinner('🔄 Vérification base de données...'):
            try:
                from database.database import init_database
                init_database()
                st.session_state.database_ready = True
                print("✅ Base de données prête")
            except Exception as e:
                st.error(f"❌ Erreur base de données: {e}")
                st.session_state.database_ready = False


def show_fallback_home():
    """Page d'accueil de fallback ultra-rapide"""
    st.title("🏠 Tableau de bord")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("👥 Consultants", "60", "Actifs")

    with col2:
        st.metric("💼 Missions", "45", "En cours")

    with col3:
        st.metric("📊 Taux", "85%", "2%")


def main():
    """Fonction principale ultra-optimisée"""

    # Header principal (instantané)
    st.markdown(
        '<div class="main-header">🏢 Consultator</div>', unsafe_allow_html=True
    )

    # Menu de navigation (affiché immédiatement)
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

    # Initialisation base de données en parallèle
    init_database_fast()

    # Chargement lazy du module sélectionné uniquement
    try:
        if selected == "🏠 Accueil":
            module = load_module_lazy('home')
            if module:
                module.show()
            else:
                show_fallback_home()

        elif selected == "👥 Consultants":
            with st.spinner('🔄 Chargement module consultants...'):
                module = load_module_lazy('consultants')
                if module:
                    module.show()
                else:
                    st.error("❌ Module Consultants non disponible")

        elif selected == "👨‍💼 Business Managers":
            with st.spinner('🔄 Chargement module business managers...'):
                module = load_module_lazy('business_managers')
                if module:
                    module.show()
                else:
                    st.error("❌ Module Business Managers non disponible")

        elif selected == "🏢 Practices":
            with st.spinner('🔄 Chargement module practices...'):
                module = load_module_lazy('practices')
                if module:
                    module.show()
                else:
                    st.error("❌ Module Practices non disponible")

        elif selected == "🔧 Technologies":
            with st.spinner('🔄 Chargement module technologies...'):
                module = load_module_lazy('technologies')
                if module:
                    module.show()
                else:
                    st.error("❌ Module Technologies non disponible")

        elif selected == "🤖 Assistant IA":
            with st.spinner('🔄 Chargement assistant IA...'):
                module = load_module_lazy('chatbot')
                if module:
                    module.show()
                else:
                    st.error("❌ Module Assistant IA non disponible")

    except Exception as e:
        st.error(f"❌ Erreur: {e}")
        import traceback
        with st.expander("🔍 Détails"):
            st.code(traceback.format_exc())


if __name__ == "__main__":
    main()
