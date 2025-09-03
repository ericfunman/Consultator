
"""
Widget de sélection de technologies avec référentiel
"""
import streamlit as st
import sys
import os
from typing import List
from services.technology_service import TechnologyService
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


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
    current_techs = []
    if current_technologies:
        current_techs_raw = [tech.strip() for tech in current_technologies.split(',') if tech.strip()]

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
                # Ajouter automatiquement comme technologie personnalisée
                if TechnologyService.add_custom_technology(tech, "Personnalisées"):
                    current_techs.append(tech)
                    # Recharger la liste des technologies
                    all_techs = TechnologyService.get_all_available_technologies()
    
    # Colonnes pour le layout
    col_main, col_add = st.columns([4, 1])
    with col_main:
        # Multiselect principal - s'assurer que les valeurs par défaut sont dans les options
        valid_current_techs = [tech for tech in current_techs if tech in all_techs]

        selected_techs = st.multiselect(
            label,
            options=all_techs,
            default=valid_current_techs,
            key=key,
            help=help_text or "Sélectionnez les technologies utilisées"
        )
        def show_technologies_referentiel():
            """Page de gestion du référentiel de technologies"""
        st.markdown("<br>", unsafe_allow_html=True)  # Espacement
        if st.button("➕ Ajouter", key=f"{key}_add_btn" if key else "add_tech_btn"):
            st.session_state[f'show_add_tech_{key}'] = True

    # Formulaire d'ajout de technologie personnalisée
    if st.session_state.get(f'show_add_tech_{key}', False):
        with st.expander("➕ Ajouter une technologie personnalisée", expanded=True):
            new_tech_name = st.text_input("Nom de la technologie", key=f"{key}_new_tech_name")
            new_tech_category = st.selectbox(
                "Catégorie",
                [
                    "Personnalisées",
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
                    "Méthodologies"
                ],
                key=f"{key}_new_tech_cat"
            )
            col_add_btn, col_cancel_btn = st.columns(2)
            with col_add_btn:
                if st.button("Ajouter", key=f"{key}_confirm_add", type="primary"):
                    if new_tech_name:
                        if TechnologyService.add_custom_technology(new_tech_name, new_tech_category):
                            st.success(f"✅ Technologie '{new_tech_name}' ajoutée !")
                            st.session_state[f'show_add_tech_{key}'] = False
                            st.rerun()
                        else:
                            st.error("❌ Cette technologie existe déjà")
                    else:
                        st.error("❌ Veuillez saisir le nom de la technologie")
            with col_cancel_btn:
                if st.button("Annuler", key=f"{key}_cancel_add"):
                    st.session_state[f'show_add_tech_{key}'] = False
                    st.rerun()

    # Retourner la chaîne des technologies sélectionnées
    return ', '.join(selected_techs)


  
def show_technologies_referentiel():
    """Page de gestion du référentiel de technologies"""
    st.subheader("🛠️ Référentiel des Technologies")
    tab1, tab2 = st.tabs(["📋 Technologies disponibles", "➕ Gérer les technologies personnalisées"])
    with tab1:
        # Affichage du référentiel par catégorie
        technologies_by_cat = TechnologyService.get_technologies_by_category()
        search_query = st.text_input("🔍 Rechercher une technologie", placeholder="Ex: Python, React, Docker...")
        if search_query:
            # Recherche
            found_techs = TechnologyService.search_technologies(search_query)
            st.write(f"**{len(found_techs)} technologie(s) trouvée(s):**")
            # Afficher en colonnes
            cols = st.columns(3)
            for i, tech in enumerate(found_techs):
                with cols[i % 3]:
                    st.write(f"• {tech}")
        else:
            # Affichage par catégorie
            for category, techs in technologies_by_cat.items():
                with st.expander(f"📂 {category} ({len(techs)} technologies)"):
                    # Afficher en colonnes
                    cols = st.columns(3)
                    for i, tech in enumerate(techs):
                        with cols[i % 3]:
                            st.write(f"• {tech}")
    with tab2:
        # Gestion des technologies personnalisées
        st.markdown("### ➕ Ajouter une technologie personnalisée")
        with st.form("add_custom_tech_form"):
            tech_name = st.text_input("Nom de la technologie")
            tech_category = st.selectbox(
                "Catégorie",
                [
                    "Personnalisées",
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
                    "Méthodologies"
                ]
            )
            st.text_area("Description (optionnel)")
            if st.form_submit_button("➕ Ajouter la technologie", type="primary"):
                if tech_name:
                    if TechnologyService.add_custom_technology(tech_name, tech_category):
                        st.success(f"✅ Technologie '{tech_name}' ajoutée avec succès !")
                        st.rerun()
                    else:
                        st.error("❌ Cette technologie existe déjà")
                else:
                    st.error("❌ Veuillez saisir le nom de la technologie")
        # Liste des technologies personnalisées
        st.markdown("---")
        st.markdown("### 📋 Technologies personnalisées existantes")
        custom_techs = TechnologyService.get_custom_technologies()
        if custom_techs:
            for tech in custom_techs:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**{tech['nom']}**")
                with col2:
                    st.write(f"*{tech['categorie']}*")
                with col3:
                    if st.button("🗑️", key=f"del_{tech['id']}", help="Supprimer"):
                        if TechnologyService.delete_custom_technology(tech['id']):
                            st.success("✅ Technologie supprimée !")
                            st.rerun()
        else:
            st.info("📝 Aucune technologie personnalisée ajoutée")
