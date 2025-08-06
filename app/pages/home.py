"""
Page d'accueil de Consultator
Dashboard principal avec statistiques et vue d'ensemble
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os

# Import des services
sys.path.append(os.path.dirname(__file__))
from database.database import get_database_session, get_database_info
from database.models import Consultant, Competence, Mission, ConsultantCompetence

def show():
    """Affiche la page d'accueil"""
    
    st.title("🏠 Tableau de bord")
    st.markdown("### Vue d'ensemble de votre practice data")
    
    # Informations sur la base de données
    db_info = get_database_info()
    
    if not db_info.get("exists", False):
        st.error("❌ Base de données non initialisée")
        if st.button("Initialiser la base de données"):
            from database.database import init_database
            if init_database():
                st.success("✅ Base de données initialisée avec succès !")
                st.rerun()
        return
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Consultants",
            value=db_info.get("consultants", 0),
            delta="Actifs dans la practice"
        )
    
    with col2:
        st.metric(
            label="🎯 Compétences",
            value=db_info.get("competences", 0),
            delta="Référentiel technique"
        )
    
    with col3:
        st.metric(
            label="💼 Missions",
            value=db_info.get("missions", 0),
            delta="En cours et terminées"
        )
    
    with col4:
        # Calculer le taux d'occupation (simulation)
        taux_occupation = 85  # À calculer dynamiquement plus tard
        st.metric(
            label="📊 Taux d'occupation",
            value=f"{taux_occupation}%",
            delta="2%" if taux_occupation > 80 else "-3%"
        )
    
    st.markdown("---")
    
    # Section graphiques si on a des données
    if db_info.get("consultants", 0) > 0:
        show_dashboard_charts()
    else:
        show_getting_started()

def show_dashboard_charts():
    """Affiche les graphiques du dashboard"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Répartition des compétences")
        
        # Créer des données de démonstration
        # TODO: Remplacer par de vraies données de la DB
        demo_data = {
            "Catégorie": ["Backend", "Frontend", "Data", "Cloud", "Mobile"],
            "Nombre": [15, 12, 8, 10, 5]
        }
        df = pd.DataFrame(demo_data)
        
        fig = px.pie(
            df, 
            values='Nombre', 
            names='Catégorie',
            title="Compétences par catégorie"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Évolution des revenus")
        
        # Données de démonstration
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        revenus = [50000 + i * 5000 + (i % 3) * 2000 for i in range(len(dates))]
        
        df_revenus = pd.DataFrame({
            'Mois': dates,
            'Revenus': revenus
        })
        
        fig = px.line(
            df_revenus,
            x='Mois',
            y='Revenus',
            title="Évolution mensuelle des revenus"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tableau des dernières activités
    st.subheader("📋 Activités récentes")
    
    # Données de démonstration
    activites = [
        {"Date": "2024-08-06", "Action": "Nouveau consultant ajouté", "Détail": "Jean Dupont - Data Analyst"},
        {"Date": "2024-08-05", "Action": "Mission terminée", "Détail": "Projet Analytics - Client ABC"},
        {"Date": "2024-08-04", "Action": "Compétence ajoutée", "Détail": "Python - Expert pour Marie Martin"},
        {"Date": "2024-08-03", "Action": "Nouvelle mission", "Détail": "DevOps - Client XYZ"},
    ]
    
    df_activites = pd.DataFrame(activites)
    st.dataframe(df_activites, use_container_width=True, hide_index=True)

def show_getting_started():
    """Affiche la section pour commencer"""
    
    st.subheader("🚀 Commencez avec Consultator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.markdown("""
            <div style="padding: 20px; border: 2px solid #1f77b4; border-radius: 10px; text-align: center;">
                <h3>👥 Étape 1</h3>
                <p><strong>Ajoutez vos consultants</strong></p>
                <p>Commencez par ajouter les profils de vos 60 consultants avec leurs informations de base.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown("""
            <div style="padding: 20px; border: 2px solid #ff7f0e; border-radius: 10px; text-align: center;">
                <h3>🎯 Étape 2</h3>
                <p><strong>Définissez les compétences</strong></p>
                <p>Associez les compétences techniques et fonctionnelles à chaque consultant.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        with st.container():
            st.markdown("""
            <div style="padding: 20px; border: 2px solid #2ca02c; border-radius: 10px; text-align: center;">
                <h3>💼 Étape 3</h3>
                <p><strong>Gérez les missions</strong></p>
                <p>Ajoutez l'historique des missions et suivez les revenus générés.</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Actions rapides
    st.subheader("⚡ Actions rapides")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Ajouter un consultant", type="primary"):
            st.switch_page("pages/consultants.py")
    
    with col2:
        if st.button("🎯 Gérer les compétences"):
            st.switch_page("pages/skills.py")
    
    with col3:
        if st.button("💼 Nouvelle mission"):
            st.switch_page("pages/missions.py")
    
    with col4:
        if st.button("📊 Voir les stats"):
            # TODO: Implémenter page de statistiques détaillées
            st.info("📊 Statistiques détaillées - À venir dans la prochaine version !")
    
    # Conseils et astuces
    st.markdown("---")
    with st.expander("💡 Conseils pour bien commencer"):
        st.markdown("""
        **📋 Checklist de démarrage :**
        
        1. **Importez vos données existantes** : Si vous avez des données dans Excel ou CSV, vous pourrez bientôt les importer
        2. **Standardisez les compétences** : Utilisez le référentiel prédéfini pour une cohérence optimale
        3. **Documentez les missions** : Plus vous ajoutez de détails, plus les analyses seront précises
        4. **Mettez à jour régulièrement** : Gardez les informations à jour pour des métriques fiables
        
        **🎯 Fonctionnalités à venir :**
        - Import/Export Excel et CSV
        - Chatbot IA pour recherche avancée
        - Rapports automatiques
        - Notifications et alertes
        """)

if __name__ == "__main__":
    show()
