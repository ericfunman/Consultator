"""
Page de gestion des technologies
Référentiel complet et gestion des technologies personnalisées
"""

import streamlit as st
from components.technology_widget import show_technologies_referentiel

def show():
    """Affiche la page de gestion des technologies"""
    
    st.title("🛠️ Gestion des Technologies")
    
    show_technologies_referentiel()

if __name__ == "__main__":
    show()
