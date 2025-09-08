#!/usr/bin/env python3
"""
Consultator - Version simplifiée sans preloading
Application Streamlit pour la gestion de consultants
"""

import importlib

import streamlit as st
from streamlit_option_menu import option_menu

# Configuration de la page
st.set_page_config(
    page_title="Consultator",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache des modules pour éviter les reimports
if 'modules_cache' not in st.session_state:
    st.session_state.modules_cache = {}


def load_module_safe(module_name):
    """Charge un module de manière sécurisée avec cache"""
    if module_name in st.session_state.modules_cache:
        return st.session_state.modules_cache[module_name]

    try:
        if module_name == 'home':
            import pages_modules.home as module
        elif module_name == 'consultants':
            import pages_modules.consultants as module
        elif module_name == 'practices':
            import pages_modules.practices as module
        elif module_name == 'technologies':
            import pages_modules.technologies as module
        elif module_name == 'business_managers':
            import pages_modules.business_managers as module
        elif module_name == 'chatbot':
            import pages_modules.chatbot as module
        else:
            return None

        # Recharger le module pour les changements en dev
        importlib.reload(module)
        st.session_state.modules_cache[module_name] = module
        return module

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du module {module_name}: {e}")
        return None


def show_navigation():
    """Affiche la navigation dans la sidebar avec option_menu"""

    # Menu de navigation dans la sidebar
    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=[
                "🏠 Accueil",
                "👥 Consultants",
                "🤵‍♂ Business Managers",
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

    # Mapping vers les noms de modules
    page_mapping = {
        "🏠 Accueil": "home",
        "👥 Consultants": "consultants",
        "🤵‍♂ Business Managers": "business_managers",
        "🏢 Practices": "practices",
        "🔧 Technologies": "technologies",
        "🤖 Assistant IA": "chatbot"
    }

    return page_mapping.get(selected, "home")


def main():
    """Fonction principale de l'application"""
    try:
        # Header principal
        st.markdown(
            '<div class="main-header">🏢 Consultator</div>', unsafe_allow_html=True
        )

        # Navigation
        current_page = show_navigation()

        # Chargement et affichage de la page
        module = load_module_safe(current_page)

        if module and hasattr(module, 'show'):
            try:
                module.show()
            except Exception as e:
                st.error(f"❌ Erreur lors de l'affichage de la page: {e}")
                st.info("🔄 Essayez de recharger la page")
                # Afficher les détails de l'erreur
                import traceback
                with st.expander("🔍 Détails de l'erreur"):
                    st.code(traceback.format_exc())
        else:
            st.error(f"❌ Module {current_page} non disponible")

            # Page de fallback
            if current_page == "home":
                show_fallback_home()
            else:
                st.title("🏠 Consultator")
                st.markdown("### Application de gestion de consultants")
                st.info("Sélectionnez une page dans le menu à gauche")

    except Exception as e:
        st.error(f"❌ Erreur critique: {e}")
        st.info("🔄 Rechargez l'application")


def show_fallback_home():
    """Page d'accueil de fallback"""
    st.title("🏠 Tableau de bord")
    st.markdown("### Vue d'ensemble de votre practice data")

    # Métriques de base
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("👥 Consultants", "1000+", "Actifs dans la practice")

    with col2:
        st.metric("💼 Missions", "500+", "En cours et terminées")

    with col3:
        st.metric("📈 Taux d'occupation", "85%", "2%")

    st.markdown("---")
    st.info("ℹ️ Page d'accueil en mode simplifié - Module home non disponible")


if __name__ == "__main__":
    main()
