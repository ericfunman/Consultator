"""
Consultator - Application de gestion de consultants
Version avec preloading intelligent en arrière-plan
Auteur: GitHub Copilot
Date: 2025-09-04
"""

import os
import queue
import sys
import threading
import time
from typing import Any
from typing import Dict
from typing import Optional

import streamlit as st
from streamlit_option_menu import option_menu

# Configuration de la page
st.set_page_config(
    page_title="Consultator",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache pour les modules chargés
if 'modules_cache' not in st.session_state:
    st.session_state.modules_cache = {}

# Cache pour les résultats de preloading
if 'preload_queue' not in st.session_state:
    st.session_state.preload_queue = queue.Queue()

    # Status du preloading
if 'preload_status' not in st.session_state:
    st.session_state.preload_status = {
        'home': 'loaded',  # Déjà chargé
        'consultants': 'pending',
        'business_managers': 'pending',
        'practices': 'pending',
        'technologies': 'pending',
        'chatbot': 'pending'
    }

if 'preload_thread_started' not in st.session_state:
    st.session_state.preload_thread_started = False


def load_module_lazy(module_name: str) -> Optional[Any]:
    """Charge un module de manière paresseuse avec cache."""
    if module_name in st.session_state.modules_cache:
        return st.session_state.modules_cache[module_name]

    try:
        if module_name == 'home':
            from pages_modules.home import show as home_show
            st.session_state.modules_cache[module_name] = home_show
            return home_show

        elif module_name == 'consultants':
            from pages_modules.consultants import show as consultants_show
            st.session_state.modules_cache[module_name] = consultants_show
            return consultants_show

        elif module_name == 'business_managers':
            from pages_modules.business_managers import show as bm_show
            st.session_state.modules_cache[module_name] = bm_show
            return bm_show

        elif module_name == 'practices':
            from pages_modules.practices import show as practices_show
            st.session_state.modules_cache[module_name] = practices_show
            return practices_show

        elif module_name == 'technologies':
            from pages_modules.technologies import show as technologies_show
            st.session_state.modules_cache[module_name] = technologies_show
            return technologies_show

        elif module_name == 'chatbot':
            from pages_modules.chatbot import show as chatbot_show
            st.session_state.modules_cache[module_name] = chatbot_show
            return chatbot_show

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du module {module_name}: {e}")
        return None


def preload_module_background(module_name: str) -> None:
    """Charge un module en arrière-plan."""
    try:
        # Simulation du chargement
        time.sleep(0.1)  # Petite pause pour éviter la surcharge

        # Chargement effectif du module
        module = load_module_lazy(module_name)

        if module:
            # Marquer comme chargé
            st.session_state.preload_status[module_name] = 'loaded'

            # Ajouter à la queue pour notification
            st.session_state.preload_queue.put(f"✅ Module {module_name} prêt")
        else:
            st.session_state.preload_status[module_name] = 'error'
            st.session_state.preload_queue.put(f"❌ Erreur module {module_name}")

    except Exception as e:
        st.session_state.preload_status[module_name] = 'error'
        st.session_state.preload_queue.put(f"❌ Erreur {module_name}: {str(e)}")


def start_background_preloading():
    """Démarre le preloading en arrière-plan."""
    if st.session_state.preload_thread_started:
        return

    st.session_state.preload_thread_started = True

    # Liste des modules à preloader par ordre de priorité
    modules_to_preload = [
        'consultants',      # Le plus utilisé en premier
        'business_managers',
        'practices',
        'technologies',
        'chatbot'
    ]

    def preload_worker():
        """Worker thread pour le preloading."""
        for module_name in modules_to_preload:
            if st.session_state.preload_status[module_name] == 'pending':
                st.session_state.preload_status[module_name] = 'loading'
                preload_module_background(module_name)
                time.sleep(0.5)  # Pause entre chaque module

    # Lancer le thread en arrière-plan
    thread = threading.Thread(target=preload_worker, daemon=True)
    thread.start()


@st.cache_data(ttl=300)
def init_database_fast():
    """Initialisation rapide de la base de données."""
    try:
        from database.database import init_database
        init_database()
        return True
    except Exception as e:
        st.error(f"❌ Erreur base de données: {e}")
        return False


def show_preload_status():
    """Affiche le statut du preloading de manière discrète."""
    # Fonction désactivée - pas d'affichage de barre de progression
    pass


def main():
    """Fonction principale avec preloading intelligent."""

    # CSS pour un style professionnel simple
    st.markdown("""
    <style>
    .main-title {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stSelectbox > label {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Titre principal simple
    st.markdown('<h1 class="main-title">💼 Consultator</h1>', unsafe_allow_html=True)

    # Initialisation base de données (rapide)
    if not init_database_fast():
        st.stop()

    # Menu de navigation dans la SIDEBAR (sans titre)
    with st.sidebar:
        selected = option_menu(menu_title=None,
                               options=["🏠 Accueil",
                                        "👥 Consultants",
                                        "🎯 Business Managers",
                                        "🏢 Practices",
                                        "💻 Technologies",
                                        "🤖 Chatbot"],
                               icons=["house",
                                      "people",
                                      "bullseye",
                                      "building",
                                      "laptop",
                                      "robot"],
                               menu_icon="cast",
                               default_index=0,
                               orientation="vertical",
                               styles={"container": {"padding": "0!important",
                                                     "background-color": "transparent"},
                                       "icon": {"color": "#1f77b4",
                                                "font-size": "18px"},
                                       "nav-link": {"font-size": "14px",
                                                    "text-align": "left",
                                                    "margin": "2px",
                                                    "padding": "8px 12px",
                                                    "--hover-color": "#e8f4ff",
                                                    "border-radius": "8px",
                                                    },
                                       "nav-link-selected": {"background-color": "#1f77b4",
                                                             "color": "white",
                                                             "font-weight": "bold"},
                                       },
                               )

    # Démarrer le preloading après l'affichage du menu
    if selected == "🏠 Accueil":
        start_background_preloading()

    # Afficher le statut du preloading
    show_preload_status()

    # Navigation vers les pages
    if selected == "🏠 Accueil":
        # Chargement immédiat de l'accueil
        home_module = load_module_lazy('home')
        if home_module:
            home_module()

    elif selected == "👥 Consultants":
        # Vérifier si déjà chargé en arrière-plan
        if st.session_state.preload_status['consultants'] == 'loaded':
            # Module déjà prêt, affichage immédiat
            consultants_module = st.session_state.modules_cache['consultants']
            consultants_module()
        else:
            # Chargement en cours ou en attente
            with st.spinner("🔄 Chargement du module Consultants..."):
                consultants_module = load_module_lazy('consultants')
                if consultants_module:
                    consultants_module()

    elif selected == "🎯 Business Managers":
        if st.session_state.preload_status['business_managers'] == 'loaded':
            bm_module = st.session_state.modules_cache['business_managers']
            bm_module()
        else:
            with st.spinner("🔄 Chargement du module Business Managers..."):
                bm_module = load_module_lazy('business_managers')
                if bm_module:
                    bm_module()

    elif selected == "🏢 Practices":
        if st.session_state.preload_status['practices'] == 'loaded':
            practices_module = st.session_state.modules_cache['practices']
            practices_module()
        else:
            with st.spinner("🔄 Chargement du module Practices..."):
                practices_module = load_module_lazy('practices')
                if practices_module:
                    practices_module()

    elif selected == "💻 Technologies":
        if st.session_state.preload_status['technologies'] == 'loaded':
            tech_module = st.session_state.modules_cache['technologies']
            tech_module()
        else:
            with st.spinner("🔄 Chargement du module Technologies..."):
                tech_module = load_module_lazy('technologies')
                if tech_module:
                    tech_module()

    elif selected == "🤖 Chatbot":
        if st.session_state.preload_status['chatbot'] == 'loaded':
            chatbot_module = st.session_state.modules_cache['chatbot']
            chatbot_module()
        else:
            with st.spinner("🔄 Chargement du module Chatbot..."):
                chatbot_module = load_module_lazy('chatbot')
                if chatbot_module:
                    chatbot_module()


if __name__ == "__main__":
    main()
