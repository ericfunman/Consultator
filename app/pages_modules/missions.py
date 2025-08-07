"""
Page de gestion des missions
CRUD pour les missions avec suivi des revenus
"""

import streamlit as st
import pandas as pd
import sys
import os

def show():
    """Affiche la page de gestion des missions"""
    
    st.title("💼 Gestion des missions")
    st.markdown("### Suivez les missions et revenus de vos consultants")
    
    # Onglets pour organiser les fonctionnalités
    tab1, tab2, tab3 = st.tabs(["📋 Missions actives", "➕ Nouvelle mission", "📈 Revenus"])
    
    with tab1:
        show_active_missions()
    
    with tab2:
        show_add_mission()
    
    with tab3:
        show_revenue_tracking()

def show_active_missions():
    """Liste des missions actives"""
    st.subheader("📋 Missions en cours")
    st.info("🚧 Liste des missions - En développement !")

def show_add_mission():
    """Formulaire d'ajout de mission"""
    st.subheader("➕ Créer une nouvelle mission")
    st.info("🚧 Formulaire de mission - À venir !")

def show_revenue_tracking():
    """Suivi des revenus"""
    st.subheader("📈 Suivi des revenus")
    st.info("🚧 Analytics revenus - Prochaine version !")

if __name__ == "__main__":
    show()
