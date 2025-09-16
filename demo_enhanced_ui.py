"""
Démonstration des améliorations UI pour Consultator
Montre l'utilisation des nouveaux composants d'interface
"""

import streamlit as st
import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ui.enhanced_ui import (
    AdvancedUIFilters,
    RealTimeSearch,
    DataTableEnhancer,
    LoadingSpinner,
    NotificationManager,
    create_enhanced_consultants_view
)
from app.services.cache_service import get_cache_stats


def main():
    """Fonction principale de démonstration"""
    st.set_page_config(
        page_title="Consultator - UI Améliorée",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🚀 Consultator - Interface Améliorée")
    st.markdown("---")

    # Menu de navigation
    menu = st.sidebar.selectbox(
        "Navigation",
        ["Vue Consultants Améliorée", "Démonstration Composants", "Statistiques Cache"]
    )

    if menu == "Vue Consultants Améliorée":
        show_enhanced_consultants_view()
    elif menu == "Démonstration Composants":
        show_component_demo()
    elif menu == "Statistiques Cache":
        show_cache_stats()


def show_enhanced_consultants_view():
    """Affiche la vue améliorée des consultants"""
    st.header("👥 Vue Consultants Améliorée")

    st.markdown("""
    Cette vue intègre toutes les améliorations UI :
    - 🔍 **Filtres avancés** dans la sidebar
    - ⚡ **Recherche en temps réel** avec debounce
    - 📊 **Tableau interactif** avec sélection
    - 🎯 **Actions contextuelles** sur les éléments sélectionnés
    - 📈 **Métriques en temps réel**
    """)

    try:
        create_enhanced_consultants_view()
    except Exception as e:
        st.error(f"Erreur lors du chargement de la vue : {str(e)}")
        st.info("Assurez-vous que la base de données est initialisée et que les services sont disponibles.")


def show_component_demo():
    """Démontre l'utilisation des différents composants"""
    st.header("🧩 Démonstration des Composants UI")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Filtres Avancés",
        "⚡ Recherche Temps Réel",
        "📊 Tableaux Améliorés",
        "🔔 Notifications"
    ])

    with tab1:
        st.subheader("Filtres Avancés")
        st.markdown("""
        Les filtres avancés permettent de :
        - Filtrer par texte (nom, email, société)
        - Filtrer par practice, grade, disponibilité
        - Filtrer par salaire et expérience
        - Filtrer par dates d'entrée
        - Réinitialiser facilement tous les filtres
        """)

        # Exemple d'utilisation
        filters = AdvancedUIFilters()
        st.code("""
# Utilisation basique
filters = AdvancedUIFilters()
applied_filters = filters.render_filters_sidebar()
filtered_data = filters.apply_filters(data)
        """)

    with tab2:
        st.subheader("Recherche en Temps Réel")
        st.markdown("""
        La recherche en temps réel offre :
        - Recherche instantanée pendant la saisie
        - Debounce pour éviter les requêtes trop fréquentes
        - Cache intelligent des résultats
        - Performance optimisée
        """)

        # Exemple d'utilisation
        search = RealTimeSearch()
        st.code("""
# Utilisation de la recherche
search = RealTimeSearch()
if search.should_search():
    results = search.search_with_cache(search_term)
        """)

    with tab3:
        st.subheader("Tableaux Améliorés")
        st.markdown("""
        Les tableaux améliorés incluent :
        - Sélection d'une ligne à la fois
        - Colonnes configurables
        - Actions contextuelles
        - Formatage automatique des données
        """)

        # Exemple d'utilisation
        st.code("""
# Affichage d'un tableau amélioré
event = DataTableEnhancer.render_enhanced_table(data)
if event.selection.rows:
    selected_item = data[event.selection.rows[0]]
    action = DataTableEnhancer.render_action_buttons(selected_item, ['view', 'edit'])
        """)

    with tab4:
        st.subheader("Système de Notifications")
        st.markdown("""
        Le système de notifications permet :
        - Messages de succès, erreur, avertissement, info
        - Durée configurable
        - Interface cohérente
        """)

        # Démonstration des notifications
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("✅ Succès"):
                NotificationManager.show_success("Opération réussie !")

        with col2:
            if st.button("❌ Erreur"):
                NotificationManager.show_error("Une erreur s'est produite")

        with col3:
            if st.button("⚠️ Avertissement"):
                NotificationManager.show_warning("Attention requise")

        with col4:
            if st.button("ℹ️ Info"):
                NotificationManager.show_info("Information importante")


def show_cache_stats():
    """Affiche les statistiques du cache"""
    st.header("📊 Statistiques du Cache")

    try:
        stats = get_cache_stats()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📦 Taille Cache", f"{stats.get('size', 0)} éléments")

        with col2:
            st.metric("⚡ Hit Rate", f"{stats.get('hit_rate', 0):.1f}%")

        with col3:
            st.metric("🔄 Requêtes", stats.get('total_requests', 0))

        with col4:
            st.metric("💾 Mémoire", f"{stats.get('memory_usage', 0):.1f} MB")

        # Graphiques détaillés
        st.subheader("Détails des Performances")

        # Simulation de données pour les graphiques
        import pandas as pd
        import numpy as np

        # Données de performance simulées
        performance_data = pd.DataFrame({
            'Temps': pd.date_range(start='2024-01-01', periods=24, freq='H'),
            'Temps_Réponse_ms': np.random.normal(20, 5, 24),
            'Utilisation_Cache_%': np.random.uniform(70, 95, 24)
        })

        col1, col2 = st.columns(2)

        with col1:
            st.line_chart(performance_data.set_index('Temps')['Temps_Réponse_ms'])

        with col2:
            st.line_chart(performance_data.set_index('Temps')['Utilisation_Cache_%'])

    except Exception as e:
        st.error(f"Erreur lors de la récupération des statistiques : {str(e)}")


if __name__ == "__main__":
    main()
