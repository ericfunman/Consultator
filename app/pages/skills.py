"""
Page de gestion des compétences
Association des compétences aux consultants avec niveaux d'expérience
"""

import streamlit as st
import pandas as pd
import sys
import os

def show():
    """Affiche la page de gestion des compétences"""
    
    st.title("🎯 Gestion des compétences")
    st.markdown("### Gérez les compétences techniques et fonctionnelles")
    
    # Onglets pour organiser les fonctionnalités
    tab1, tab2, tab3 = st.tabs(["📊 Vue d'ensemble", "➕ Ajouter compétences", "🔍 Recherche"])
    
    with tab1:
        show_skills_overview()
    
    with tab2:
        show_add_skills()
    
    with tab3:
        show_skills_search()

def show_skills_overview():
    """Vue d'ensemble des compétences"""
    st.subheader("📊 Répartition des compétences")
    st.info("🚧 Page en cours de développement - Prochaine version !")

def show_add_skills():
    """Formulaire d'ajout de compétences"""
    st.subheader("➕ Associer des compétences")
    st.info("🚧 Formulaire d'ajout - À venir !")

def show_skills_search():
    """Recherche de compétences"""
    st.subheader("🔍 Rechercher par compétence")
    st.info("🚧 Moteur de recherche - En développement !")

if __name__ == "__main__":
    show()
