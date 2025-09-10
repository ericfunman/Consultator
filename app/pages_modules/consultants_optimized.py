"""
Page de gestion des consultants - Version optimisée pour 1000+ consultants
CRUD complet avec pagination efficace, cache et recherche optimisée
"""

import os
import sys
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional

import pandas as pd
import streamlit as st

# Configuration des imports optimisés
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Imports avec gestion d'erreurs
try:
    from config.performance import CACHE_CONFIG
    from config.performance import PAGINATION_CONFIG
    from config.performance import get_optimal_page_size
    from config.performance import is_large_dataset
    from database.database import get_database_session
    from database.models import BusinessManager
    from database.models import Competence
    from database.models import Consultant
    from database.models import ConsultantCompetence
    from database.models import Mission
    from database.models import Practice
    from services.consultant_service import ConsultantService

    imports_ok = True
except ImportError:
    imports_ok = False


@st.cache_data(ttl=CACHE_CONFIG["stats_ttl"])
def get_dashboard_stats() -> Dict:
    """Récupère les statistiques du tableau de bord avec cache optimisé"""
    if not imports_ok:
        return {}

    try:
        return ConsultantService.get_consultant_summary_stats()
    except Exception as e:
        st.error(f"Erreur stats: {e}")
        return {}


@st.cache_data(ttl=CACHE_CONFIG["default_ttl"])
def get_consultants_paginated(
    page: int = 1, search_term: str = "", per_page: int = 50
) -> Dict:
    """Récupère les consultants avec pagination et cache"""
    if not imports_ok:
        return {"consultants": [], "total": 0, "pages": 0}

    try:
        if search_term:
            consultants = ConsultantService.search_consultants_optimized(
                search_term, page, per_page
            )
        else:
            consultants = ConsultantService.get_all_consultants(page, per_page)

        total = ConsultantService.get_consultants_count()
        pages = (total + per_page - 1) // per_page

        return {
            "consultants": consultants,
            "total": total,
            "pages": pages,
            "current_page": page,
            "per_page": per_page,
        }
    except Exception as e:
        st.error(f"Erreur récupération consultants: {e}")
        return {"consultants": [], "total": 0, "pages": 0}


def show_performance_info():
    """Affiche les informations de performance pour les gros volumes"""
    dataset_info = is_large_dataset()

    if dataset_info.get("is_large", False):
        with st.expander("⚡ Informations de performance", expanded=False):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("👥 Consultants", dataset_info.get("consultants_count", 0))
            with col2:
                st.metric("🎯 Missions", dataset_info.get("missions_count", 0))
            with col3:
                st.metric(
                    "⚡ Optimisations",
                    (
                        "✅ Activées"
                        if dataset_info.get("optimizations_enabled")
                        else "❌ Désactivées"
                    ),
                )

            st.info(
                "🚀 Optimisations activées pour gérer efficacement un grand volume de données"
            )


def show_consultants_dashboard():
    """Affiche le tableau de bord optimisé"""
    st.subheader("📊 Tableau de bord")

    stats = get_dashboard_stats()

    if stats:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "👥 Total Consultants",
                stats.get("total_consultants", 0),
                help="Nombre total de consultants dans la base",
            )

        with col2:
            st.metric(
                "✅ Disponibles",
                stats.get("available_consultants", 0),
                help="Consultants actuellement disponibles",
            )

        with col3:
            st.metric(
                "🎯 Missions Actives",
                stats.get("active_missions", 0),
                help="Missions en cours d'exécution",
            )

        with col4:
            st.metric(
                "💼 En Mission",
                stats.get("busy_consultants", 0),
                help="Consultants actuellement en mission",
            )


def show_consultants_list_optimized():
    """Affiche la liste des consultants avec pagination optimisée"""
    st.subheader("📋 Liste des consultants")

    # Barre de recherche optimisée
    col_search, col_filters = st.columns([3, 1])

    with col_search:
        search_term = st.text_input(
            "🔍 Rechercher un consultant",
            placeholder="Nom, prénom ou email...",
            help="Recherche optimisée pour de gros volumes",
        )

    with col_filters:
        show_available_only = st.checkbox(
            "✅ Disponibles uniquement", help="Filtrer les consultants disponibles"
        )

    # Configuration de la pagination
    if "consultant_page" not in st.session_state:
        st.session_state.consultant_page = 1

    # Récupération des données avec cache
    per_page = get_optimal_page_size(get_dashboard_stats().get("total_consultants", 50))
    data = get_consultants_paginated(
        page=st.session_state.consultant_page,
        search_term=search_term,
        per_page=per_page,
    )

    consultants = data["consultants"]
    total = data["total"]
    pages = data["pages"]

    # Affichage des informations de pagination
    if total > 0:
        col_info, col_nav = st.columns([2, 1])

        with col_info:
            start_idx = ((st.session_state.consultant_page - 1) * per_page) + 1
            end_idx = min(st.session_state.consultant_page * per_page, total)
            st.caption(f"📄 Affichage {start_idx}-{end_idx} sur {total} consultants")

        with col_nav:
            col_prev, col_page, col_next = st.columns(3)

            with col_prev:
                if st.button(
                    "⬅️ Précédent", disabled=(st.session_state.consultant_page <= 1)
                ):
                    st.session_state.consultant_page -= 1
                    st.rerun()

            with col_page:
                st.write(f"Page {st.session_state.consultant_page}/{pages}")

            with col_next:
                if st.button(
                    "➡️ Suivant", disabled=(st.session_state.consultant_page >= pages)
                ):
                    st.session_state.consultant_page += 1
                    st.rerun()

    # Affichage de la liste sous forme de tableau optimisé
    if consultants:
        df_display = pd.DataFrame(consultants)

        # Sélection des colonnes à afficher
        columns_to_show = [
            "id",
            "prenom",
            "nom",
            "email",
            "practice_name",
            "disponibilite",
        ]
        if all(col in df_display.columns for col in columns_to_show):
            df_filtered = df_display[columns_to_show].copy()

            # Renommage des colonnes pour l'affichage
            df_filtered.columns = [
                "ID",
                "Prénom",
                "Nom",
                "Email",
                "Practice",
                "Disponible",
            ]

            # Application du filtre disponibilité
            if show_available_only:
                df_filtered = df_filtered[df_filtered["Disponible"]]

            # Configuration de l'affichage du dataframe
            st.dataframe(
                df_filtered,
                use_container_width=True,
                height=400,
                column_config={
                    "ID": st.column_config.NumberColumn("ID", width="small"),
                    "Disponible": st.column_config.CheckboxColumn("Disponible"),
                    "Email": st.column_config.TextColumn("Email", width="medium"),
                    "Practice": st.column_config.TextColumn("Practice", width="medium"),
                },
            )

            # Actions rapides sur la sélection
            st.subheader("⚡ Actions rapides")
            col_actions = st.columns(4)

            with col_actions[0]:
                if st.button("📊 Exporter cette page"):
                    csv = df_filtered.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="💾 Télécharger CSV",
                        data=csv,
                        file_name=f"consultants_page_{
                            st.session_state.consultant_page}.csv",
                        mime="text/csv",
                    )

            with col_actions[1]:
                if st.button("🔄 Actualiser"):
                    get_consultants_paginated.clear()
                    get_dashboard_stats.clear()
                    st.rerun()

    else:
        if search_term:
            st.info(f"🔍 Aucun consultant trouvé pour '{search_term}'")
        else:
            st.info("📭 Aucun consultant dans la base de données")


def show_quick_add_consultant():
    """Formulaire d'ajout rapide de consultant optimisé"""
    st.subheader("➕ Ajout rapide de consultant")

    with st.form("quick_add_consultant", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            prenom = st.text_input("Prénom*")
            nom = st.text_input("Nom*")
            email = st.text_input("Email*")

        with col2:
            telephone = st.text_input("Téléphone")
            salaire = st.number_input(
                "Salaire (€)", min_value=0, value=45000, step=1000
            )
            disponible = st.checkbox("Disponible", value=True)

        submitted = st.form_submit_button("✅ Ajouter le consultant")

        if submitted:
            if prenom and nom and email:
                data = {
                    "prenom": prenom,
                    "nom": nom,
                    "email": email,
                    "telephone": telephone,
                    "salaire": salaire,
                    "disponible": disponible,
                    "practice_id": None,  # À améliorer avec un sélecteur
                }

                if ConsultantService.create_consultant(data):
                    st.success(f"✅ Consultant {prenom} {nom} ajouté avec succès!")
                    # Vider le cache pour afficher le nouveau consultant
                    get_consultants_paginated.clear()
                    get_dashboard_stats.clear()
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de l'ajout du consultant")
            else:
                st.error("❌ Veuillez remplir tous les champs obligatoires")


def show():
    """Page principale des consultants optimisée pour 1000+ consultants"""

    if not imports_ok:
        st.error("❌ Les services de base ne sont pas disponibles")
        st.info("Vérifiez que tous les modules sont correctement installés")
        return

    # En-tête avec informations de performance
    st.title("👥 Gestion des consultants")
    st.markdown("### 🚀 Interface optimisée pour de gros volumes")

    show_performance_info()

    # Tableau de bord
    show_consultants_dashboard()

    st.divider()

    # Organisation en onglets optimisés
    tab1, tab2, tab3 = st.tabs(
        ["📋 Liste et recherche", "➕ Ajout rapide", "📊 Statistiques détaillées"]
    )

    with tab1:
        show_consultants_list_optimized()

    with tab2:
        show_quick_add_consultant()

    with tab3:
        show_detailed_statistics()


def show_detailed_statistics():
    """Affiche des statistiques détaillées avec cache"""
    st.subheader("📊 Statistiques détaillées")

    stats = get_dashboard_stats()

    if not stats:
        st.info("📊 Statistiques en cours de chargement...")
        return

    # Graphiques de répartition
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Répartition par disponibilité")

        availability_data = {
            "Disponibles": stats.get("available_consultants", 0),
            "En mission": stats.get("busy_consultants", 0),
        }

        if sum(availability_data.values()) > 0:
            st.bar_chart(availability_data)
        else:
            st.info("Pas de données disponibles")

    with col2:
        st.subheader("🎯 Activité des missions")

        mission_data = {
            "Missions actives": stats.get("active_missions", 0),
            "Total missions": stats.get("total_missions", 0)
            - stats.get("active_missions", 0),
        }

        if sum(mission_data.values()) > 0:
            st.bar_chart(mission_data)
        else:
            st.info("Pas de données de missions")

    # Métriques de performance
    st.subheader("⚡ Métriques de performance")

    col_metrics = st.columns(3)

    with col_metrics[0]:
        avg_missions = stats.get("total_missions", 0) / max(
            stats.get("total_consultants", 1), 1
        )
        st.metric("📊 Missions/Consultant", f"{avg_missions:.1f}")

    with col_metrics[1]:
        utilization = (
            stats.get("busy_consultants", 0) / max(stats.get("total_consultants", 1), 1)
        ) * 100
        st.metric("📈 Taux d'utilisation", f"{utilization:.1f}%")

    with col_metrics[2]:
        if stats.get("total_consultants", 0) >= 1000:
            st.metric("🎯 Volume", "Gros volume", delta="Optimisé")
        else:
            st.metric("🎯 Volume", "Standard")


if __name__ == "__main__":
    show()
