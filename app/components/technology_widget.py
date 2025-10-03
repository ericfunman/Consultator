"""
Widget de sélection de technologies avec référentiel
"""

import os
import sys
from typing import List

import streamlit as st

from services.technology_service import TechnologyService

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Constantes pour les catégories
TECHNOLOGY_CATEGORIES = [
    "Personnalisés",
    "Langages de programmation",
    "Frameworks Web",
    "Bases de données",
    "Cloud & DevOps",
    "Intelligence Artificielle & Data Science",
    "Mobile",
    "Outils de développement",
    "Architecture & Design",
    "Sécurité",
    "Systèmes d'exploitation",
    "Méthodologies",
]


def _parse_current_technologies(current_technologies: str, all_techs: list) -> list:
    """Parse et valide les technologies actuelles"""
    if not current_technologies:
        return []

    current_techs = []
    current_techs_raw = [tech.strip() for tech in current_technologies.split(",") if tech.strip()]

    # Matcher les technologies actuelles avec celles disponibles (insensible à la casse)
    all_techs_lower = {tech.lower(): tech for tech in all_techs}

    for tech in current_techs_raw:
        # Chercher une correspondance exacte d'abord
        if tech in all_techs:
            current_techs.append(tech)
        # Sinon chercher une correspondance insensible à la casse
        elif tech.lower() in all_techs_lower:
            current_techs.append(all_techs_lower[tech.lower()])
        # Si pas de correspondance, ajouter la technologie personnalisée
        else:
            _add_custom_technology_if_needed(tech)
            current_techs.append(tech)

    return current_techs


def _add_custom_technology_if_needed(tech_name: str) -> bool:
    """Ajoute une technologie personnalisée si elle n'existe pas"""
    return TechnologyService.add_custom_technology(tech_name, "Personnalisés")


def _render_add_technology_form(key: str) -> None:
    """Affiche le formulaire d'ajout de technologie"""
    if not st.session_state.get(f"show_add_tech_{key}", False):
        return

    with st.expander("⚡ Ajouter une technologie personnalisée", expanded=True):
        new_tech_name = st.text_input("Nom de la technologie", key=f"{key}_new_tech_name")
        new_tech_category = st.selectbox(
            "Catégorie",
            TECHNOLOGY_CATEGORIES,
            key=f"{key}_new_tech_cat",
        )

        col_add_btn, col_cancel_btn = st.columns(2)
        with col_add_btn:
            if st.button("Ajouter", key=f"{key}_confirm_add", type="primary"):
                _handle_add_technology(new_tech_name, new_tech_category, key)

        with col_cancel_btn:
            if st.button("Annuler", key=f"{key}_cancel_add"):
                st.session_state[f"show_add_tech_{key}"] = False
                st.rerun()


def _handle_add_technology(tech_name: str, category: str, key: str) -> None:
    """Gère l'ajout d'une nouvelle technologie"""
    if not tech_name:
        st.error("⚠️ Veuillez saisir le nom de la technologie")
        return

    if TechnologyService.add_custom_technology(tech_name, category):
        st.success(f"✅ Technologie '{tech_name}' ajoutée !")
        st.session_state[f"show_add_tech_{key}"] = False
        st.rerun()
    else:
        st.error("❌ Cette technologie existe déjà")


def technology_multiselect(label: str, current_technologies: str = "", key: str = None, help_text: str = None) -> str:
    """
    Widget de sélection multiple de technologies avec possibilité d'ajout

    Args:
        label: Label du widget
        current_technologies: Technologies actuelles (chaîne séparée par des virgules)
        key: Clé unique pour le widget
        help_text: Texte d'aide

    Returns:
        String des technologies sélectionnées séparées par des virgules
    """
    # Récupérer toutes les technologies disponibles
    all_techs = TechnologyService.get_all_available_technologies()

    # Parser les technologies actuelles
    current_techs = _parse_current_technologies(current_technologies, all_techs)

    # Recharger si des technologies ont été ajoutées
    if len(current_techs) > 0:
        all_techs = TechnologyService.get_all_available_technologies()

    # Interface utilisateur
    selected_techs = _render_multiselect_interface(label, all_techs, current_techs, key, help_text)

    # Formulaire d'ajout si activé
    _render_add_technology_form(key)

    # Retourner la chaîne des technologies sélectionnées
    return ", ".join(selected_techs)


def _render_multiselect_interface(label: str, all_techs: list, current_techs: list, key: str, help_text: str) -> list:
    """Affiche l'interface de sélection multiple"""
    # Colonnes pour le layout
    col_main, _ = st.columns([4, 1])

    with col_main:
        # Multiselect principal - s'assurer que les valeurs par défaut sont dans les options
        valid_current_techs = [tech for tech in current_techs if tech in all_techs]

        selected_techs = st.multiselect(
            label,
            options=all_techs,
            default=valid_current_techs,
            key=key,
            help=help_text or "Sélectionnez les technologies utilisées",
        )

        st.markdown("<br>", unsafe_allow_html=True)  # Espacement
        if st.button("⚡ Ajouter", key=f"{key}_add_btn" if key else "add_tech_btn"):
            st.session_state[f"show_add_tech_{key}"] = True

        return selected_techs

    return []


def _render_technologies_search_tab():
    """Affiche l'onglet de recherche de technologies"""
    technologies_by_cat = TechnologyService.get_technologies_by_category()
    search_query = st.text_input("🔍 Rechercher une technologie", placeholder="Ex: Python, React, Docker...")

    if search_query:
        _display_search_results(search_query)
    else:
        _display_technologies_by_category(technologies_by_cat)


def _display_search_results(search_query: str):
    """Affiche les résultats de recherche"""
    found_techs = TechnologyService.search_technologies(search_query)
    st.write(f"**{len(found_techs)} technologie(s) trouvée(s):**")

    # Afficher en colonnes
    cols = st.columns(3)
    for i, tech in enumerate(found_techs):
        with cols[i % 3]:
            st.write(f"⚡ {tech}")


def _display_technologies_by_category(technologies_by_cat: dict):
    """Affiche les technologies par catégorie"""
    for category, techs in technologies_by_cat.items():
        with st.expander(f"📁 {category} ({len(techs)} technologies)"):
            # Afficher en colonnes
            cols = st.columns(3)
            for i, tech in enumerate(techs):
                with cols[i % 3]:
                    st.write(f"⚡ {tech}")


def _render_add_technology_tab():
    """Affiche l'onglet d'ajout de technologies personnalisées"""
    st.markdown("### ⚡ Ajouter une technologie personnalisée")

    _render_add_technology_form_main()

    st.markdown("---")
    st.markdown("### 📋 Technologies personnalisées existantes")
    _display_custom_technologies_list()


def _render_add_technology_form_main():
    """Affiche le formulaire principal d'ajout de technologie"""
    with st.form("add_custom_tech_form"):
        tech_name = st.text_input("Nom de la technologie")
        tech_category = st.selectbox("Catégorie", TECHNOLOGY_CATEGORIES)
        st.text_area("Description (optionnel)")

        if st.form_submit_button("⚡ Ajouter la technologie", type="primary"):
            _handle_form_submission(tech_name, tech_category)


def _handle_form_submission(tech_name: str, tech_category: str):
    """Gère la soumission du formulaire d'ajout"""
    if not tech_name:
        st.error("⚠️ Veuillez saisir le nom de la technologie")
        return

    if TechnologyService.add_custom_technology(tech_name, tech_category):
        st.success(f"✅ Technologie '{tech_name}' ajoutée avec succès !")
        st.rerun()
    else:
        st.error("❌ Cette technologie existe déjà")


def _display_custom_technologies_list():
    """Affiche la liste des technologies personnalisées"""
    custom_techs = TechnologyService.get_custom_technologies()

    if not custom_techs:
        st.info("ℹ️ Aucune technologie personnalisée ajoutée")
        return

    for tech in custom_techs:
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"**{tech['nom']}**")
        with col2:
            st.write(f"*{tech['categorie']}*")
        with col3:
            if st.button("🗑️", key=f"del_{tech['id']}", help="Supprimer"):
                _handle_delete_technology(tech["id"])


def _handle_delete_technology(tech_id: int):
    """Gère la suppression d'une technologie"""
    if TechnologyService.delete_custom_technology(tech_id):
        st.success("✅ Technologie supprimée !")
        st.rerun()


def show_technologies_referentiel():
    """Page de gestion du référentiel de technologies"""
    st.subheader("📚 Référentiel des Technologies")

    tab1, tab2 = st.tabs(["📖 Technologies disponibles", "⚙️ Gérer les technologies personnalisées"])

    with tab1:
        _render_technologies_search_tab()

    with tab2:
        _render_add_technology_tab()
