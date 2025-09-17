"""
Widget de slection de technologies avec rfrentiel
"""

import os
import sys
from typing import List

import streamlit as st

from services.technology_service import TechnologyService

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def technology_multiselect(
    label: str, current_technologies: str = "", key: str = None, help_text: str = None
) -> str:
    """
    Widget de slection multiple de technologies avec possibilit d'ajout

    Args:
        label: Label du widget
        current_technologies: Technologies actuelles (chane spare par des virgules)
        key: Cl unique pour le widget
        help_text: Texte d'aide

    Returns:
        String des technologies slectionnes spares par des virgules
    """

    # Rcuprer toutes les technologies disponibles
    all_techs = TechnologyService.get_all_available_technologies()

    # Parser les technologies actuelles
    current_techs = []
    if current_technologies:
        current_techs_raw = [
            tech.strip() for tech in current_technologies.split(",") if tech.strip()
        ]

        # Matcher les technologies actuelles avec celles disponibles (insensible 
        # la casse)
        all_techs_lower = {tech.lower(): tech for tech in all_techs}

        for tech in current_techs_raw:
            # Chercher une correspondance exacte d'abord
            if tech in all_techs:
                current_techs.append(tech)
            # Sinon chercher une correspondance insensible  la casse
            elif tech.lower() in all_techs_lower:
                current_techs.append(all_techs_lower[tech.lower()])
            # Si pas de correspondance, ajouter la technologie personnalise
            else:
                # Ajouter automatiquement comme technologie personnalise
                if TechnologyService.add_custom_technology(tech, "Personnalises"):
                    current_techs.append(tech)
                    # Recharger la liste des technologies
                    all_techs = TechnologyService.get_all_available_technologies()

    # Colonnes pour le layout
    col_main, col_add = st.columns([4, 1])
    with col_main:
        # Multiselect principal - s'assurer que les valeurs par dfaut sont dans
        # les options
        valid_current_techs = [tech for tech in current_techs if tech in all_techs]

        selected_techs = st.multiselect(
            label,
            options=all_techs,
            default=valid_current_techs,
            key=key,
            help=help_text or "Slectionnez les technologies utilises",
        )

        def show_technologies_referentiel():
            """Page de gestion du rfrentiel de technologies"""

        st.markdown("<br>", unsafe_allow_html=True)  # Espacement
        if st.button(" Ajouter", key=f"{key}_add_btn" if key else "add_tech_btn"):
            st.session_state[f"show_add_tech_{key}"] = True

    # Formulaire d'ajout de technologie personnalise
    if st.session_state.get(f"show_add_tech_{key}", False):
        with st.expander(" Ajouter une technologie personnalise", expanded=True):
            new_tech_name = st.text_input(
                "Nom de la technologie", key=f"{key}_new_tech_name"
            )
            new_tech_category = st.selectbox(
                "Catgorie",
                [
                    "Personnalises",
                    "Langages de programmation",
                    "Frameworks Web",
                    "Bases de donnes",
                    "Cloud & DevOps",
                    "Intelligence Artificielle & Data Science",
                    "Mobile",
                    "Outils de dveloppement",
                    "Architecture & Design",
                    "Scurit",
                    "Systmes d'exploitation",
                    "Mthodologies",
                ],
                key=f"{key}_new_tech_cat",
            )
            col_add_btn, col_cancel_btn = st.columns(2)
            with col_add_btn:
                if st.button("Ajouter", key=f"{key}_confirm_add", type="primary"):
                    if new_tech_name:
                        if TechnologyService.add_custom_technology(
                            new_tech_name, new_tech_category
                        ):
                            st.success(f" Technologie '{new_tech_name}' ajoute !")
                            st.session_state[f"show_add_tech_{key}"] = False
                            st.rerun()
                        else:
                            st.error(" Cette technologie existe dj")
                    else:
                        st.error(" Veuillez saisir le nom de la technologie")
            with col_cancel_btn:
                if st.button("Annuler", key=f"{key}_cancel_add"):
                    st.session_state[f"show_add_tech_{key}"] = False
                    st.rerun()

    # Retourner la chane des technologies slectionnes
    return ", ".join(selected_techs)


def show_technologies_referentiel():
    """Page de gestion du rfrentiel de technologies"""
    st.subheader(" Rfrentiel des Technologies")
    tab1, tab2 = st.tabs(
        [" Technologies disponibles", " Grer les technologies personnalises"]
    )
    with tab1:
        # Affichage du rfrentiel par catgorie
        technologies_by_cat = TechnologyService.get_technologies_by_category()
        search_query = st.text_input(
            " Rechercher une technologie", placeholder="Ex: Python, React, Docker..."
        )
        if search_query:
            # Recherche
            found_techs = TechnologyService.search_technologies(search_query)
            st.write(f"**{len(found_techs)} technologie(s) trouve(s):**")
            # Afficher en colonnes
            cols = st.columns(3)
            for i, tech in enumerate(found_techs):
                with cols[i % 3]:
                    st.write(f" {tech}")
        else:
            # Affichage par catgorie
            for category, techs in technologies_by_cat.items():
                with st.expander(f" {category} ({len(techs)} technologies)"):
                    # Afficher en colonnes
                    cols = st.columns(3)
                    for i, tech in enumerate(techs):
                        with cols[i % 3]:
                            st.write(f" {tech}")
    with tab2:
        # Gestion des technologies personnalises
        st.markdown("###  Ajouter une technologie personnalise")
        with st.form("add_custom_tech_form"):
            tech_name = st.text_input("Nom de la technologie")
            tech_category = st.selectbox(
                "Catgorie",
                [
                    "Personnalises",
                    "Langages de programmation",
                    "Frameworks Web",
                    "Bases de donnes",
                    "Cloud & DevOps",
                    "Intelligence Artificielle & Data Science",
                    "Mobile",
                    "Outils de dveloppement",
                    "Architecture & Design",
                    "Scurit",
                    "Systmes d'exploitation",
                    "Mthodologies",
                ],
            )
            st.text_area("Description (optionnel)")
            if st.form_submit_button(" Ajouter la technologie", type="primary"):
                if tech_name:
                    if TechnologyService.add_custom_technology(
                        tech_name, tech_category
                    ):
                        st.success(
                            f" Technologie '{tech_name}' ajoute avec succs !"
                        )
                        st.rerun()
                    else:
                        st.error(" Cette technologie existe dj")
                else:
                    st.error(" Veuillez saisir le nom de la technologie")
        # Liste des technologies personnalises
        st.markdown("---")
        st.markdown("###  Technologies personnalises existantes")
        custom_techs = TechnologyService.get_custom_technologies()
        if custom_techs:
            for tech in custom_techs:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**{tech['nom']}**")
                with col2:
                    st.write(f"*{tech['categorie']}*")
                with col3:
                    if st.button("", key=f"del_{tech['id']}", help="Supprimer"):
                        if TechnologyService.delete_custom_technology(tech["id"]):
                            st.success(" Technologie supprime !")
                            st.rerun()
        else:
            st.info(" Aucune technologie personnalise ajoute")
