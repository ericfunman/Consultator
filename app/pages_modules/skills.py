"""
Page Compétences
Gestion des compétences des consultants
"""

import streamlit as st


def show():
    """Affiche la page de gestion des compétences"""
    st.title("🎯 Gestion des Compétences")

    tab1, tab2 = st.tabs(["Vue d'ensemble", "Gestion détaillée"])

    with tab1:
        show_skills_overview()

    with tab2:
        show_skills_management()


def show_skills_overview():
    """Affiche la vue d'ensemble des compétences"""
    st.subheader("📊 Vue d'ensemble des compétences")

    # Placeholder pour la vue d'ensemble
    st.info("🚧 Fonctionnalité en développement")


def show_skills_management():
    """Affiche la gestion détaillée des compétences"""
    st.subheader("⚙️ Gestion détaillée des compétences")

    # Placeholder pour la gestion détaillée
    st.info("🚧 Fonctionnalité en développement")
