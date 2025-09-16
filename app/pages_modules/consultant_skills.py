"""
Module de gestion des compétences du consultant
Fonctions pour afficher, ajouter et modifier les compétences
"""

import os
import sys
from typing import Any
from typing import Dict
from typing import List

import streamlit as st

# Ajouter les chemins nécessaires
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Variables pour les imports
ConsultantService = None
get_database_session = None
Consultant = None
imports_ok = False

try:
    from database.database import get_database_session
    from database.models import Competence
    from database.models import Consultant
    from database.models import ConsultantCompetence
    from services.consultant_service import ConsultantService
    from utils.skill_categories import SKILL_CATEGORIES

    imports_ok = True
except ImportError:
    # Imports échoués, on continue quand même
    pass


def show_consultant_skills(consultant):
    """Affiche les compétences du consultant"""

    if not imports_ok:
        st.error("❌ Les services de base ne sont pas disponibles")
        return

    if not consultant:
        st.error("❌ Consultant non fourni")
        return

    st.markdown("### 💼 Compétences")

    try:
        # Récupérer les compétences du consultant
        with get_database_session() as session:
            consultant_competences = (
                session.query(ConsultantCompetence)
                .join(Competence)
                .filter(ConsultantCompetence.consultant_id == consultant.id)
                .all()
            )

        if not consultant_competences:
            st.info("ℹ️ Aucune compétence enregistrée pour ce consultant")
            show_add_skill_form(consultant.id)
            return

        # Organiser les compétences par catégorie
        skills_by_category = {}
        for cc in consultant_competences:
            category = cc.competence.categorie or "Autre"
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(
                {
                    "id": cc.id,
                    "nom": cc.competence.nom,
                    "niveau": cc.niveau,
                    "annees_experience": cc.annees_experience,
                    "certification": cc.certification,
                    "date_acquisition": cc.date_acquisition,
                }
            )

        # Afficher les compétences par catégorie
        for category, skills in skills_by_category.items():
            st.markdown(f"#### 🏷️ {category}")

            # Créer un tableau pour cette catégorie
            skill_data = []
            for skill in skills:
                skill_data.append(
                    {
                        "Compétence": skill["nom"],
                        "Niveau": get_niveau_label(skill["niveau"]),
                        "Expérience": (
                            f"{skill['annees_experience']} an(s)"
                            if skill["annees_experience"]
                            else "N/A"
                        ),
                        "Certification": "✅" if skill["certification"] else "❌",
                        "Actions": f"edit_{skill['id']}",
                    }
                )

            import pandas as pd

            df = pd.DataFrame(skill_data)

            # Afficher le tableau avec actions
            for index, row in df.iterrows():
                col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])

                with col1:
                    st.write(f"**{row['Compétence']}**")

                with col2:
                    st.write(row["Niveau"])

                with col3:
                    st.write(row["Expérience"])

                with col4:
                    st.write(row["Certification"])

                with col5:
                    skill_id = row["Actions"].replace("edit_", "")
                    if st.button("✏️", key=f"edit_skill_{skill_id}", help="Modifier"):
                        st.session_state.edit_skill = int(skill_id)
                        st.rerun()
                    if st.button("🗑️", key=f"delete_skill_{skill_id}", help="Supprimer"):
                        if delete_skill(int(skill_id)):
                            st.rerun()

        # Statistiques des compétences
        show_skills_statistics(consultant_competences)

        # Actions générales
        st.markdown("#### 🎯 Actions")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("➕ Ajouter compétence", key=f"add_skill_{consultant.id}"):
                st.session_state.add_skill = consultant.id
                st.rerun()

        with col2:
            if st.button(
                "📊 Analyse compétences",
                key=f"analyze_skills_{consultant.id}",
            ):
                show_skills_analysis(consultant_competences)

        with col3:
            if st.button("📈 Évolution", key=f"skills_evolution_{consultant.id}"):
                show_skills_evolution(consultant.id)

        # Formulaire d'ajout (si activé)
        if (
            "add_skill" in st.session_state
            and st.session_state.add_skill == consultant.id
        ):
            show_add_skill_form(consultant.id)

        # Formulaire de modification (si activé)
        if "edit_skill" in st.session_state:
            show_edit_skill_form(st.session_state.edit_skill)

    except Exception as e:
        st.error(f"❌ Erreur lors de l'affichage des compétences: {e}")
        st.code(str(e))


def get_niveau_label(niveau: int) -> str:
    """Retourne le label du niveau de compétence"""

    niveaux = {1: "Débutant", 2: "Intermédiaire", 3: "Avancé", 4: "Expert", 5: "Maître"}
    return niveaux.get(niveau, f"Niveau {niveau}")


def show_skills_statistics(consultant_competences):
    """Affiche les statistiques des compétences"""

    if not consultant_competences:
        return

    st.markdown("#### 📊 Statistiques")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_skills = len(consultant_competences)
        st.metric("Total compétences", total_skills)

    with col2:
        avg_level = sum(cc.niveau for cc in consultant_competences) / len(
            consultant_competences
        )
        st.metric("Niveau moyen", f"{avg_level:.1f}/5")

    with col3:
        certified_count = sum(1 for cc in consultant_competences if cc.certification)
        st.metric("Certifiées", certified_count)

    with col4:
        avg_experience = sum(
            cc.annees_experience or 0 for cc in consultant_competences
        ) / len(consultant_competences)
        st.metric("Expérience moyenne", f"{avg_experience:.1f} ans")


def show_add_skill_form(consultant_id: int):
    """Affiche le formulaire d'ajout de compétence"""

    st.markdown("### ➕ Ajouter une compétence")

    try:
        # Récupérer les compétences disponibles
        with get_database_session() as session:
            existing_competences = (
                session.query(ConsultantCompetence)
                .filter(ConsultantCompetence.consultant_id == consultant_id)
                .all()
            )

            existing_skill_ids = [cc.competence_id for cc in existing_competences]

            available_competences = (
                session.query(Competence)
                .filter(~Competence.id.in_(existing_skill_ids))
                .all()
            )

        if not available_competences:
            st.warning(
                "⚠️ Toutes les compétences existantes sont déjà associées à ce consultant"
            )
            return

        with st.form(f"add_skill_form_{consultant_id}", clear_on_submit=True):
            # Sélection de la compétence
            skill_options = {
                c.id: f"{
                    c.nom} ({
                    c.categorie})"
                for c in available_competences
            }
            selected_skill = st.selectbox(
                "Compétence *",
                options=list(skill_options.keys()),
                format_func=lambda x: skill_options[x],
                help="Sélectionnez une compétence à ajouter",
            )

            col1, col2 = st.columns(2)

            with col1:
                niveau = st.slider(
                    "Niveau *",
                    min_value=1,
                    max_value=5,
                    value=3,
                    help="Niveau de maîtrise (1=Débutant, 5=Expert)",
                )

                certification = st.checkbox(
                    "Certification",
                    help="Le consultant possède-t-il une certification ?",
                )

            with col2:
                annees_experience = st.number_input(
                    "Années d'expérience",
                    min_value=0,
                    max_value=50,
                    value=0,
                    help="Nombre d'années d'expérience dans cette compétence",
                )

            # Boutons
            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                submitted = st.form_submit_button("💾 Ajouter", type="primary")

            with col2:
                cancel = st.form_submit_button("❌ Annuler")

            with col3:
                pass

            if submitted:
                success = add_skill_to_consultant(
                    consultant_id,
                    {
                        "competence_id": selected_skill,
                        "niveau": niveau,
                        "annees_experience": annees_experience,
                        "certification": certification,
                    },
                )

                if success:
                    st.success("✅ Compétence ajoutée avec succès !")
                    if "add_skill" in st.session_state:
                        del st.session_state.add_skill
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de l'ajout de la compétence")

            if cancel:
                if "add_skill" in st.session_state:
                    del st.session_state.add_skill
                st.rerun()

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du formulaire: {e}")


def add_skill_to_consultant(consultant_id: int, data: Dict[str, Any]) -> bool:
    """Ajoute une compétence au consultant"""

    try:
        with get_database_session() as session:
            # Vérifier que la compétence n'existe pas déjà
            existing = (
                session.query(ConsultantCompetence)
                .filter(
                    ConsultantCompetence.consultant_id == consultant_id,
                    ConsultantCompetence.competence_id == data["competence_id"],
                )
                .first()
            )

            if existing:
                st.error("❌ Cette compétence est déjà associée au consultant")
                return False

            # Créer la nouvelle association
            from datetime import datetime

            consultant_competence = ConsultantCompetence(
                consultant_id=consultant_id,
                competence_id=data["competence_id"],
                niveau=data["niveau"],
                annees_experience=data["annees_experience"],
                certification=data["certification"],
                date_acquisition=datetime.now(),
            )

            session.add(consultant_competence)
            session.commit()

            return True

    except Exception as e:
        st.error(f"❌ Erreur lors de l'ajout de la compétence: {e}")
        return False


def show_edit_skill_form(consultant_competence_id: int):
    """Affiche le formulaire de modification de compétence"""

    st.markdown("### ✏️ Modifier une compétence")

    try:
        with get_database_session() as session:
            cc = (
                session.query(ConsultantCompetence)
                .join(Competence)
                .filter(ConsultantCompetence.id == consultant_competence_id)
                .first()
            )

            if not cc:
                st.error("❌ Compétence introuvable")
                return

        with st.form(
            f"edit_skill_form_{consultant_competence_id}", clear_on_submit=False
        ):
            st.write(f"**Compétence :** {cc.competence.nom}")

            col1, col2 = st.columns(2)

            with col1:
                niveau = st.slider(
                    "Niveau *",
                    min_value=1,
                    max_value=5,
                    value=cc.niveau,
                    help="Niveau de maîtrise (1=Débutant, 5=Expert)",
                )

                certification = st.checkbox(
                    "Certification",
                    value=cc.certification,
                    help="Le consultant possède-t-il une certification ?",
                )

            with col2:
                annees_experience = st.number_input(
                    "Années d'expérience",
                    min_value=0,
                    max_value=50,
                    value=cc.annees_experience or 0,
                    help="Nombre d'années d'expérience dans cette compétence",
                )

            # Boutons
            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                submitted = st.form_submit_button("💾 Enregistrer", type="primary")

            with col2:
                cancel = st.form_submit_button("❌ Annuler")

            with col3:
                pass

            if submitted:
                success = update_consultant_skill(
                    consultant_competence_id,
                    {
                        "niveau": niveau,
                        "annees_experience": annees_experience,
                        "certification": certification,
                    },
                )

                if success:
                    st.success("✅ Compétence mise à jour avec succès !")
                    if "edit_skill" in st.session_state:
                        del st.session_state.edit_skill
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de la mise à jour")

            if cancel:
                if "edit_skill" in st.session_state:
                    del st.session_state.edit_skill
                st.rerun()

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du formulaire de modification: {e}")


def update_consultant_skill(
    consultant_competence_id: int, data: Dict[str, Any]
) -> bool:
    """Met à jour une compétence du consultant"""

    try:
        with get_database_session() as session:
            cc = (
                session.query(ConsultantCompetence)
                .filter(ConsultantCompetence.id == consultant_competence_id)
                .first()
            )

            if not cc:
                st.error("❌ Compétence introuvable")
                return False

            # Mettre à jour les données
            cc.niveau = data["niveau"]
            cc.annees_experience = data["annees_experience"]
            cc.certification = data["certification"]

            session.commit()

            return True

    except Exception as e:
        st.error(f"❌ Erreur lors de la mise à jour de la compétence: {e}")
        return False


def delete_skill(consultant_competence_id: int) -> bool:
    """Supprime une compétence du consultant"""

    try:
        with get_database_session() as session:
            cc = (
                session.query(ConsultantCompetence)
                .filter(ConsultantCompetence.id == consultant_competence_id)
                .first()
            )

            if not cc:
                st.error("❌ Compétence introuvable")
                return False

            session.delete(cc)
            session.commit()

            st.info("✅ Compétence supprimée")
            return True

    except Exception as e:
        st.error(f"❌ Erreur lors de la suppression de la compétence: {e}")
        return False


def show_skills_analysis(consultant_competences):
    """Affiche une analyse des compétences"""

    st.markdown("### 📊 Analyse des compétences")

    if not consultant_competences:
        st.info("ℹ️ Aucune compétence à analyser")
        return

    # Analyse par niveau
    level_counts = {}
    for cc in consultant_competences:
        level = cc.niveau
        level_counts[level] = level_counts.get(level, 0) + 1

    # Analyse par catégorie
    category_counts = {}
    for cc in consultant_competences:
        category = cc.competence.categorie or "Autre"
        category_counts[category] = category_counts.get(category, 0) + 1

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📈 Répartition par niveau")
        for level in range(1, 6):
            count = level_counts.get(level, 0)
            if count > 0:
                st.write(f"**{get_niveau_label(level)} :** {count}")

    with col2:
        st.markdown("#### 🏷️ Répartition par catégorie")
        for category, count in category_counts.items():
            st.write(f"**{category} :** {count}")

    # Recommandations
    st.markdown("#### 💡 Recommandations")

    # Identifier les points forts et faibles
    strong_skills = [cc for cc in consultant_competences if cc.niveau >= 4]
    weak_skills = [cc for cc in consultant_competences if cc.niveau <= 2]

    if strong_skills:
        st.success(
            f"✅ **Points forts :** {len(strong_skills)} compétence(s) de haut niveau"
        )

    if weak_skills:
        st.warning(f"⚠️ **À développer :** {len(weak_skills)} compétence(s) à renforcer")

    # Certifications
    certified_count = sum(1 for cc in consultant_competences if cc.certification)
    if certified_count > 0:
        st.info(f"📜 **Certifications :** {certified_count} compétence(s) certifiée(s)")


def show_skills_evolution(consultant_id: int):
    """Affiche l'évolution des compétences dans le temps"""

    st.markdown("### 📈 Évolution des compétences")

    try:
        with get_database_session() as session:
            # Récupérer l'historique des compétences (basé sur les dates d'acquisition)
            consultant_competences = (
                session.query(ConsultantCompetence)
                .join(Competence)
                .filter(ConsultantCompetence.consultant_id == consultant_id)
                .order_by(ConsultantCompetence.date_ajout)
                .all()
            )

        if not consultant_competences:
            st.info("ℹ️ Aucune donnée d'évolution disponible")
            return

        # Grouper par année
        evolution_data = {}
        for cc in consultant_competences:
            if cc.date_acquisition:
                year = cc.date_acquisition.year
                if year not in evolution_data:
                    evolution_data[year] = []
                evolution_data[year].append(cc)

        # Afficher l'évolution
        for year in sorted(evolution_data.keys()):
            st.markdown(f"#### 📅 {year}")
            skills = evolution_data[year]

            for skill in skills:
                col1, col2, col3 = st.columns([3, 2, 2])

                with col1:
                    st.write(f"**{skill.competence.nom}**")

                with col2:
                    st.write(f"Niveau {skill.niveau}")

                with col3:
                    if skill.date_acquisition:
                        st.write(skill.date_acquisition.strftime("%d/%m"))

    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse de l'évolution: {e}")
