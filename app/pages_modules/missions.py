"""
Page Missions
Gestion des missions des consultants
"""

import streamlit as st


def show():
    """Affiche la page de gestion des missions"""
    st.title("📋 Gestion des Missions")

    tab1, tab2 = st.tabs(["Liste des missions", "Ajouter une mission"])

    with tab1:
        show_missions_list()

    with tab2:
        show_add_mission_form()


def show_missions_list():
    """Affiche la liste des missions"""
    st.subheader("📋 Liste des missions")

    # Placeholder pour la liste des missions
    st.info("🚧 Fonctionnalité en développement")


def show_add_mission_form():
    """Affiche le formulaire d'ajout de mission"""
    st.subheader("➕ Ajouter une mission")

    # Placeholder pour le formulaire
    st.info("🚧 Fonctionnalité en développement")
