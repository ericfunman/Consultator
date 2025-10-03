"""
Améliorations de l'interface utilisateur pour Consultator
Filtres avancés, recherche en temps réel, et UX améliorée
"""

import time
from datetime import date
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import pandas as pd
import streamlit as st

from app.services.cache_service import get_cached_consultants_list
from app.services.cache_service import get_cached_search_results
from app.services.consultant_service import ConsultantService

# Constantes pour les labels d'interface
LABEL_SOCIETE = "Société"
LABEL_PRENOM = "Prénom"
LABEL_SALAIRE_ACTUEL = "Salaire Actuel"
LABEL_ANNEES_EXP = "Années Exp."


class AdvancedUIFilters:
    """Classe pour gérer les filtres avancés de l'interface utilisateur"""

    def __init__(self):
        self.filters = {
            "search_term": "",
            "practice_filter": None,
            "grade_filter": None,
            "availability_filter": None,
            "salaire_min": None,
            "salaire_max": None,
            "experience_min": None,
            "experience_max": None,
            "societe_filter": None,
            "type_contrat_filter": None,
            "date_entree_min": None,
            "date_entree_max": None,
        }

    def render_filters_sidebar(self) -> Dict[str, Any]:
        """Affiche les filtres dans la sidebar et retourne les valeurs filtrées"""
        st.sidebar.header("🔍 Filtres Avancés")

        # Recherche textuelle
        self.filters["search_term"] = st.sidebar.text_input(
            "Rechercher",
            placeholder="Nom, prénom, email, société...",
            help="Recherche dans tous les champs textuels",
        )

        st.sidebar.markdown("---")

        # Filtres de statut
        st.sidebar.subheader("📊 Statut")

        col1, col2 = st.sidebar.columns(2)

        def format_availability(availability_value):
            """Formate la valeur de disponibilité pour l'affichage"""
            if availability_value is None:
                return "Tous"
            return "Disponible" if availability_value else "Occupé"

        with col1:
            self.filters["availability_filter"] = st.sidebar.selectbox(
                "Disponibilité",
                options=[None, True, False],
                format_func=format_availability,
                help="Filtrer par disponibilité",
            )

        with col2:
            self.filters["practice_filter"] = st.sidebar.selectbox(
                "Practice",
                options=[None] + self._get_unique_values("practice_name"),
                help="Filtrer par practice",
            )

        # Filtres professionnels
        st.sidebar.subheader("💼 Profil Professionnel")

        col1, col2 = st.sidebar.columns(2)
        with col1:
            self.filters["grade_filter"] = st.sidebar.selectbox(
                "Grade",
                options=[None] + self._get_unique_values("grade"),
                help="Filtrer par grade",
            )

        with col2:
            self.filters["type_contrat_filter"] = st.sidebar.selectbox(
                "Type de contrat",
                options=[None] + self._get_unique_values("type_contrat"),
                help="Filtrer par type de contrat",
            )

        self.filters["societe_filter"] = st.sidebar.selectbox(
            LABEL_SOCIETE,
            options=[None] + self._get_unique_values("societe"),
            help="Filtrer par société",
        )

        # Filtres de salaire
        st.sidebar.subheader("💰 Salaire (€)")

        col1, col2 = st.sidebar.columns(2)
        with col1:
            self.filters["salaire_min"] = st.sidebar.number_input(
                "Min", min_value=0, value=0, step=5000, help="Salaire minimum annuel"
            )

        with col2:
            self.filters["salaire_max"] = st.sidebar.number_input(
                "Max",
                min_value=0,
                value=200000,
                step=5000,
                help="Salaire maximum annuel",
            )

        # Filtres d'expérience
        st.sidebar.subheader("📅 Expérience (années)")

        col1, col2 = st.sidebar.columns(2)
        with col1:
            self.filters["experience_min"] = st.sidebar.number_input(
                "Min",
                min_value=0.0,
                max_value=50.0,
                value=0.0,
                step=0.5,
                help="Expérience minimum en années",
            )

        with col2:
            self.filters["experience_max"] = st.sidebar.number_input(
                "Max",
                min_value=0.0,
                max_value=50.0,
                value=50.0,
                step=0.5,
                help="Expérience maximum en années",
            )

        # Filtres de date d'entrée
        st.sidebar.subheader("📅 Date d'entrée société")

        col1, col2 = st.sidebar.columns(2)
        with col1:
            self.filters["date_entree_min"] = st.sidebar.date_input("De", value=None, help="Date d'entrée minimum")

        with col2:
            self.filters["date_entree_max"] = st.sidebar.date_input("À", value=None, help="Date d'entrée maximum")

        # Boutons d'action
        st.sidebar.markdown("---")

        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.sidebar.button("🔄 Réinitialiser", width="stretch"):
                self.reset_filters()
                st.rerun()

        with col2:
            if st.sidebar.button("📊 Appliquer", type="primary", width="stretch"):
                st.rerun()

        return self.filters

    def _get_unique_values(self, field: str) -> List[str]:
        """Récupère les valeurs uniques pour un champ donné"""
        try:
            # Pour les données de test, on retourne des valeurs par défaut
            # En production, ceci serait récupéré de la base de données
            defaults = {
                "practice_name": ["Digital", "Data", "Cloud", "Cybersecurity"],
                "grade": ["Junior", "Confirmé", "Senior", "Expert"],
                "type_contrat": ["CDI", "CDD", "Freelance", "Stagiaire"],
                "societe": ["Quanteam", "Asigma", "Autres"],
            }
            return defaults.get(field, [])
        except Exception:
            return []

    def reset_filters(self):
        """Réinitialise tous les filtres"""
        for key in self.filters:
            if key.endswith("_filter") or key.endswith("_min") or key.endswith("_max"):
                self.filters[key] = None
            elif key == "search_term":
                self.filters[key] = ""
            elif key in ["salaire_min", "experience_min"]:
                self.filters[key] = 0
            elif key == "salaire_max":
                self.filters[key] = 200000
            elif key == "experience_max":
                self.filters[key] = 50.0

    def apply_filters(self, data: List[Dict]) -> List[Dict]:
        """Applique les filtres aux données"""
        if not data:
            return data

        filtered_data = data.copy()

        # Filtre de recherche textuelle
        if self.filters["search_term"]:
            search_term = self.filters["search_term"].lower()
            filtered_data = [
                item
                for item in filtered_data
                if any(search_term in str(value).lower() for value in item.values() if value)
            ]

        # Filtres spécifiques
        if self.filters["practice_filter"]:
            filtered_data = [
                item for item in filtered_data if item.get("practice_name") == self.filters["practice_filter"]
            ]

        if self.filters["grade_filter"]:
            filtered_data = [item for item in filtered_data if item.get("grade") == self.filters["grade_filter"]]

        if self.filters["availability_filter"] is not None:
            filtered_data = [
                item for item in filtered_data if item.get("disponibilite") == self.filters["availability_filter"]
            ]

        if self.filters["societe_filter"]:
            filtered_data = [item for item in filtered_data if item.get("societe") == self.filters["societe_filter"]]

        if self.filters["type_contrat_filter"]:
            filtered_data = [
                item for item in filtered_data if item.get("type_contrat") == self.filters["type_contrat_filter"]
            ]

        # Filtres de salaire
        if self.filters["salaire_min"] is not None:
            filtered_data = [
                item for item in filtered_data if item.get("salaire_actuel", 0) >= self.filters["salaire_min"]
            ]

        if self.filters["salaire_max"] is not None:
            filtered_data = [
                item for item in filtered_data if item.get("salaire_actuel", 0) <= self.filters["salaire_max"]
            ]

        # Filtres d'expérience
        if self.filters["experience_min"] is not None:
            filtered_data = [
                item for item in filtered_data if item.get("experience_annees", 0) >= self.filters["experience_min"]
            ]

        if self.filters["experience_max"] is not None:
            filtered_data = [
                item for item in filtered_data if item.get("experience_annees", 0) <= self.filters["experience_max"]
            ]

        return filtered_data


class RealTimeSearch:
    """Classe pour gérer la recherche en temps réel"""

    def __init__(self):
        self.last_search_time = 0
        self.search_debounce_ms = 300  # 300ms de debounce

    def should_search(self) -> bool:
        """Détermine si une nouvelle recherche doit être effectuée"""
        current_time = time.time() * 1000  # en millisecondes
        if current_time - self.last_search_time > self.search_debounce_ms:
            self.last_search_time = current_time
            return True
        return False

    def search_with_cache(self, search_term: str, page: int = 1, per_page: int = 50):
        """Effectue une recherche avec cache"""
        if not search_term.strip():
            return get_cached_consultants_list(page, per_page)

        return get_cached_search_results(search_term.strip(), page, per_page)


class DataTableEnhancer:
    """Classe pour améliorer l'affichage des tableaux de données"""

    @staticmethod
    def render_enhanced_table(data: List[Dict], key_prefix: str = "table") -> Optional[Dict]:
        """Affiche un tableau amélioré avec sélection et actions"""
        if not data:
            st.info("📝 Aucune donnée à afficher")
            return None

        # Convertir en DataFrame pour un meilleur affichage
        df = pd.DataFrame(data)

        # Renommer les colonnes pour un meilleur affichage
        column_mapping = {
            "id": "ID",
            "prenom": LABEL_PRENOM,
            "nom": "Nom",
            "email": "Email",
            "telephone": "Téléphone",
            "salaire_actuel": LABEL_SALAIRE_ACTUEL,
            "disponibilite": "Disponible",
            "practice_name": "Practice",
            "grade": "Grade",
            "type_contrat": "Contrat",
            "societe": LABEL_SOCIETE,
            "experience_annees": LABEL_ANNEES_EXP,
            "nb_missions": "Missions",
            "cjm_formatted": "CJM",
            "salaire_formatted": "Salaire Formaté",
            "experience_formatted": "Expérience Formatée",
            "statut": "Statut",
        }

        # Appliquer le mapping des colonnes
        df = df.rename(columns=column_mapping)

        # Sélectionner les colonnes à afficher
        display_columns = [
            "ID",
            LABEL_PRENOM,
            "Nom",
            "Email",
            LABEL_SOCIETE,
            "Grade",
            "Contrat",
            LABEL_SALAIRE_ACTUEL,
            "CJM",
            LABEL_ANNEES_EXP,
            "Statut",
            "Missions",
        ]

        # Garder seulement les colonnes qui existent
        available_columns = [col for col in display_columns if col in df.columns]
        df_display = df[available_columns]

        # Configuration du tableau
        event = st.dataframe(
            df_display,
            width="stretch",
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            column_config={
                "ID": st.column_config.NumberColumn("ID", width="small"),
                LABEL_PRENOM: st.column_config.TextColumn(LABEL_PRENOM, width="medium"),
                "Nom": st.column_config.TextColumn("Nom", width="medium"),
                "Email": st.column_config.TextColumn("Email", width="large"),
                LABEL_SALAIRE_ACTUEL: st.column_config.TextColumn(LABEL_SALAIRE_ACTUEL, width="medium"),
                "CJM": st.column_config.TextColumn("CJM", width="medium"),
                LABEL_ANNEES_EXP: st.column_config.TextColumn(LABEL_ANNEES_EXP, width="small"),
                "Missions": st.column_config.NumberColumn("Missions", width="small"),
            },
        )

        return event

    @staticmethod
    def render_action_buttons(selected_data: Dict, actions: List[str]) -> Optional[str]:
        """Affiche les boutons d'action pour l'élément sélectionné"""
        if not selected_data:
            return None

        st.success(f"✅ Sélectionné : {selected_data.get('prenom', '')} {selected_data.get('nom', '')}")

        col1, col2, col3 = st.columns(3)

        action_performed = None

        with col1:
            if "view" in actions and st.button("👁️ Voir profil", type="primary", width="stretch"):
                action_performed = "view"

        with col2:
            if "edit" in actions and st.button("✏️ Modifier", width="stretch"):
                action_performed = "edit"

        with col3:
            if "delete" in actions and st.button("🗑️ Supprimer", width="stretch"):
                action_performed = "delete"

        return action_performed


class LoadingSpinner:
    """Classe pour gérer les indicateurs de chargement"""

    @staticmethod
    def show_loading(text: str = "Chargement en cours..."):
        """Affiche un spinner de chargement"""
        return st.spinner(text)

    @staticmethod
    def show_progress(current: int, total: int, text: str = "Traitement en cours..."):
        """Affiche une barre de progression"""
        progress_bar = st.progress(0, text=text)
        progress_bar.progress(current / total if total > 0 else 0)
        return progress_bar


class NotificationManager:
    """Classe pour gérer les notifications utilisateur"""

    @staticmethod
    def show_success(message: str, duration: int = 3):
        """Affiche une notification de succès"""
        st.success(message)
        if duration > 0:
            time.sleep(duration)
            st.empty()

    @staticmethod
    def show_error(message: str, duration: int = 5):
        """Affiche une notification d'erreur"""
        st.error(message)
        if duration > 0:
            time.sleep(duration)
            st.empty()

    @staticmethod
    def show_warning(message: str, duration: int = 4):
        """Affiche une notification d'avertissement"""
        st.warning(message)
        if duration > 0:
            time.sleep(duration)
            st.empty()

    @staticmethod
    def show_info(message: str, duration: int = 3):
        """Affiche une notification d'information"""
        st.info(message)
        if duration > 0:
            time.sleep(duration)
            st.empty()


# Fonctions utilitaires pour une utilisation facile
def create_enhanced_consultants_view():
    """Crée une vue améliorée de la liste des consultants"""
    # Initialiser les composants
    filters, search, enhancer = _initialize_ui_components()

    # Afficher les filtres dans la sidebar
    applied_filters = filters.render_filters_sidebar()

    # Titre principal
    st.title("👥 Gestion des consultants - Version Améliorée")

    # Recherche et chargement des données
    data = _load_consultant_data(search)

    # Appliquer les filtres
    if applied_filters:
        data = filters.apply_filters(data)

    # Afficher les métriques et le tableau
    _display_metrics(data)
    event = enhancer.render_enhanced_table(data, "consultants")

    # Gérer les actions sur la sélection
    _handle_consultant_selection(event, data, enhancer)


def _initialize_ui_components():
    """Initialise les composants de l'interface utilisateur"""
    filters = AdvancedUIFilters()
    search = RealTimeSearch()
    enhancer = DataTableEnhancer()
    return filters, search, enhancer


def _load_consultant_data(search):
    """Charge les données des consultants avec recherche"""
    # Recherche en temps réel
    search_term = st.text_input(
        "🔍 Recherche en temps réel",
        placeholder="Tapez pour rechercher instantanément...",
        help="La recherche se met à jour automatiquement pendant que vous tapez",
    )

    # Chargement des données avec cache
    with st.spinner("Chargement des données..."):
        if search_term and search.should_search():
            return search.search_with_cache(search_term)
        else:
            return get_cached_consultants_list()


def _display_metrics(data):
    """Affiche les métriques des consultants"""
    if not data:
        return

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Total", len(data))

    with col2:
        disponibles = len([c for c in data if c.get("disponibilite", False)])
        st.metric("✅ Disponibles", disponibles)

    with col3:
        st.metric("🔴 Occupés", len(data) - disponibles)

    with col4:
        salaire_moyen = sum(c.get("salaire_actuel", 0) for c in data) / len(data) if data else 0
        st.metric("💰 Salaire moyen", f"{salaire_moyen:,.0f}€")


def _handle_consultant_selection(event, data, enhancer):
    """Gère les actions sur la sélection de consultant"""
    if not event or not event.selection.rows:
        return

    selected_idx = event.selection.rows[0]
    if selected_idx >= len(data):
        return

    selected_consultant = data[selected_idx]
    action = enhancer.render_action_buttons(selected_consultant, ["view", "edit", "delete"])

    _execute_consultant_action(action, selected_consultant)


def _execute_consultant_action(action, selected_consultant):
    """Exécute l'action sélectionnée sur le consultant"""
    if action in ["view", "edit"]:
        st.session_state.view_consultant_profile = selected_consultant["id"]
        st.rerun()
    elif action == "delete":
        if ConsultantService.delete_consultant(selected_consultant["id"]):
            NotificationManager.show_success("Consultant supprimé avec succès!")
            st.rerun()
        else:
            NotificationManager.show_error("Erreur lors de la suppression")


# Export des classes pour utilisation externe
__all__ = [
    "AdvancedUIFilters",
    "RealTimeSearch",
    "DataTableEnhancer",
    "LoadingSpinner",
    "NotificationManager",
    "create_enhanced_consultants_view",
]
