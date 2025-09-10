"""
Module de gestion des langues du consultant
Fonctions pour afficher, ajouter et modifier les langues
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
    from database.models import Consultant
    from database.models import ConsultantLangue
    from database.models import Langue
    from services.consultant_service import ConsultantService

    imports_ok = True
except ImportError:
    # Imports échoués, on continue quand même
    pass


def show_consultant_languages(consultant):
    """Affiche les langues du consultant"""

    if not imports_ok:
        st.error("❌ Les services de base ne sont pas disponibles")
        return

    if not consultant:
        st.error("❌ Consultant non fourni")
        return

    st.markdown("### 🌍 Langues")

    try:
        # Récupérer les langues du consultant
        with get_database_session() as session:
            consultant_langues = (
                session.query(ConsultantLangue)
                .join(Langue)
                .filter(ConsultantLangue.consultant_id == consultant.id)
                .all()
            )

        if not consultant_langues:
            st.info("ℹ️ Aucune langue enregistrée pour ce consultant")
            show_add_language_form(consultant.id)
            return

        # Créer un tableau des langues
        language_data = []
        for cl in consultant_langues:
            language_data.append(
                {
                    "id": cl.id,
                    "Langue": cl.langue.nom,
                    "Niveau": get_niveau_label(cl.niveau),
                    "Niveau écrit": (
                        get_niveau_label(cl.niveau_ecrit) if cl.niveau_ecrit else "N/A"
                    ),
                    "Niveau parlé": (
                        get_niveau_label(cl.niveau_parle) if cl.niveau_parle else "N/A"
                    ),
                    "Certification": "✅" if cl.certification else "❌",
                    "Langue maternelle": "✅" if cl.langue_maternelle else "❌",
                }
            )

        import pandas as pd

        df = pd.DataFrame(language_data)

        # Afficher le tableau avec actions
        st.dataframe(
            df[
                [
                    "Langue",
                    "Niveau",
                    "Niveau écrit",
                    "Niveau parlé",
                    "Certification",
                    "Langue maternelle",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

        # Actions sur chaque langue
        st.markdown("#### 🎯 Actions par langue")

        for index, row in df.iterrows():
            col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 2, 2, 2, 2, 2, 2])

            with col1:
                st.write(f"**{row['Langue']}**")

            with col2:
                st.write(row["Niveau"])

            with col3:
                st.write(row["Niveau écrit"])

            with col4:
                st.write(row["Niveau parlé"])

            with col5:
                st.write(row["Certification"])

            with col6:
                st.write(row["Langue maternelle"])

            with col7:
                language_id = row["id"]
                if st.button("✏️", key=f"edit_lang_{language_id}", help="Modifier"):
                    st.session_state.edit_language = language_id
                    st.rerun()
                if st.button("🗑️", key=f"delete_lang_{language_id}", help="Supprimer"):
                    if delete_language(language_id):
                        st.rerun()

        # Statistiques des langues
        show_languages_statistics(consultant_langues)

        # Actions générales
        st.markdown("#### 🎯 Actions générales")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("➕ Ajouter langue", key=f"add_lang_{consultant.id}"):
                st.session_state.add_language = consultant.id
                st.rerun()

        with col2:
            if st.button("📊 Analyse langues", key=f"analyze_lang_{consultant.id}"):
                show_languages_analysis(consultant_langues)

        with col3:
            if st.button("🌍 Comparaison", key=f"compare_lang_{consultant.id}"):
                show_languages_comparison(consultant.id)

        # Formulaire d'ajout (si activé)
        if (
            "add_language" in st.session_state
            and st.session_state.add_language == consultant.id
        ):
            show_add_language_form(consultant.id)

        # Formulaire de modification (si activé)
        if "edit_language" in st.session_state:
            show_edit_language_form(st.session_state.edit_language)

    except Exception as e:
        st.error(f"❌ Erreur lors de l'affichage des langues: {e}")
        st.code(str(e))


def get_niveau_label(niveau: int) -> str:
    """Retourne le label du niveau de langue"""

    niveaux = {
        1: "A1 - Débutant",
        2: "A2 - Élémentaire",
        3: "B1 - Intermédiaire",
        4: "B2 - Intermédiaire avancé",
        5: "C1 - Autonome",
        6: "C2 - Maîtrise",
    }
    return niveaux.get(niveau, f"Niveau {niveau}")


def show_languages_statistics(consultant_langues):
    """Affiche les statistiques des langues"""

    if not consultant_langues:
        return

    st.markdown("#### 📊 Statistiques")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_languages = len(consultant_langues)
        st.metric("Total langues", total_languages)

    with col2:
        native_count = sum(1 for cl in consultant_langues if cl.langue_maternelle)
        st.metric("Langues maternelles", native_count)

    with col3:
        certified_count = sum(1 for cl in consultant_langues if cl.certification)
        st.metric("Certifiées", certified_count)

    with col4:
        avg_level = sum(cl.niveau for cl in consultant_langues) / len(
            consultant_langues
        )
        st.metric("Niveau moyen", f"{avg_level:.1f}/6")


def show_add_language_form(consultant_id: int):
    """Affiche le formulaire d'ajout de langue"""

    st.markdown("### ➕ Ajouter une langue")

    try:
        # Récupérer les langues disponibles
        with get_database_session() as session:
            existing_langues = (
                session.query(ConsultantLangue)
                .filter(ConsultantLangue.consultant_id == consultant_id)
                .all()
            )

            existing_lang_ids = [cl.langue_id for cl in existing_langues]

            available_langues = (
                session.query(Langue).filter(~Langue.id.in_(existing_lang_ids)).all()
            )

        if not available_langues:
            st.warning(
                "⚠️ Toutes les langues existantes sont déjà associées à ce consultant"
            )
            return

        with st.form(f"add_language_form_{consultant_id}", clear_on_submit=True):
            # Sélection de la langue
            lang_options = {langue.id: langue.nom for langue in available_langues}
            selected_lang = st.selectbox(
                "Langue *",
                options=list(lang_options.keys()),
                format_func=lambda x: lang_options[x],
                help="Sélectionnez une langue à ajouter",
            )

            col1, col2 = st.columns(2)

            with col1:
                niveau_general = st.slider(
                    "Niveau général *",
                    min_value=1,
                    max_value=6,
                    value=3,
                    help="Niveau général de maîtrise (1=A1, 6=C2)",
                )

                niveau_ecrit = st.slider(
                    "Niveau écrit",
                    min_value=1,
                    max_value=6,
                    value=3,
                    help="Niveau spécifique en expression écrite",
                )

            with col2:
                niveau_parle = st.slider(
                    "Niveau parlé",
                    min_value=1,
                    max_value=6,
                    value=3,
                    help="Niveau spécifique en expression orale",
                )

                langue_maternelle = st.checkbox(
                    "Langue maternelle",
                    help="Cette langue est-elle la langue maternelle du consultant ?",
                )

            certification = st.checkbox(
                "Certification",
                help="Le consultant possède-t-il une certification pour cette langue ?",
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
                success = add_language_to_consultant(
                    consultant_id,
                    {
                        "langue_id": selected_lang,
                        "niveau": niveau_general,
                        "niveau_ecrit": niveau_ecrit,
                        "niveau_parle": niveau_parle,
                        "certification": certification,
                        "langue_maternelle": langue_maternelle,
                    },
                )

                if success:
                    st.success("✅ Langue ajoutée avec succès !")
                    if "add_language" in st.session_state:
                        del st.session_state.add_language
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de l'ajout de la langue")

            if cancel:
                if "add_language" in st.session_state:
                    del st.session_state.add_language
                st.rerun()

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du formulaire: {e}")


def add_language_to_consultant(consultant_id: int, data: Dict[str, Any]) -> bool:
    """Ajoute une langue au consultant"""

    try:
        with get_database_session() as session:
            # Vérifier que la langue n'existe pas déjà
            existing = (
                session.query(ConsultantLangue)
                .filter(
                    ConsultantLangue.consultant_id == consultant_id,
                    ConsultantLangue.langue_id == data["langue_id"],
                )
                .first()
            )

            if existing:
                st.error("❌ Cette langue est déjà associée au consultant")
                return False

            # Créer la nouvelle association
            consultant_langue = ConsultantLangue(
                consultant_id=consultant_id,
                langue_id=data["langue_id"],
                niveau=data["niveau"],
                niveau_ecrit=data["niveau_ecrit"],
                niveau_parle=data["niveau_parle"],
                certification=data["certification"],
                langue_maternelle=data["langue_maternelle"],
            )

            session.add(consultant_langue)
            session.commit()

            return True

    except Exception as e:
        st.error(f"❌ Erreur lors de l'ajout de la langue: {e}")
        return False


def show_edit_language_form(consultant_langue_id: int):
    """Affiche le formulaire de modification de langue"""

    st.markdown("### ✏️ Modifier une langue")

    try:
        with get_database_session() as session:
            cl = (
                session.query(ConsultantLangue)
                .join(Langue)
                .filter(ConsultantLangue.id == consultant_langue_id)
                .first()
            )

            if not cl:
                st.error("❌ Langue introuvable")
                return

        with st.form(
            f"edit_language_form_{consultant_langue_id}", clear_on_submit=False
        ):
            st.write(f"**Langue :** {cl.langue.nom}")

            col1, col2 = st.columns(2)

            with col1:
                niveau_general = st.slider(
                    "Niveau général *",
                    min_value=1,
                    max_value=6,
                    value=cl.niveau,
                    help="Niveau général de maîtrise (1=A1, 6=C2)",
                )

                niveau_ecrit = st.slider(
                    "Niveau écrit",
                    min_value=1,
                    max_value=6,
                    value=cl.niveau_ecrit or 3,
                    help="Niveau spécifique en expression écrite",
                )

            with col2:
                niveau_parle = st.slider(
                    "Niveau parlé",
                    min_value=1,
                    max_value=6,
                    value=cl.niveau_parle or 3,
                    help="Niveau spécifique en expression orale",
                )

                langue_maternelle = st.checkbox(
                    "Langue maternelle",
                    value=cl.langue_maternelle,
                    help="Cette langue est-elle la langue maternelle du consultant ?",
                )

            certification = st.checkbox(
                "Certification",
                value=cl.certification,
                help="Le consultant possède-t-il une certification pour cette langue ?",
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
                success = update_consultant_language(
                    consultant_langue_id,
                    {
                        "niveau": niveau_general,
                        "niveau_ecrit": niveau_ecrit,
                        "niveau_parle": niveau_parle,
                        "certification": certification,
                        "langue_maternelle": langue_maternelle,
                    },
                )

                if success:
                    st.success("✅ Langue mise à jour avec succès !")
                    if "edit_language" in st.session_state:
                        del st.session_state.edit_language
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de la mise à jour")

            if cancel:
                if "edit_language" in st.session_state:
                    del st.session_state.edit_language
                st.rerun()

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du formulaire de modification: {e}")


def update_consultant_language(consultant_langue_id: int, data: Dict[str, Any]) -> bool:
    """Met à jour une langue du consultant"""

    try:
        with get_database_session() as session:
            cl = (
                session.query(ConsultantLangue)
                .filter(ConsultantLangue.id == consultant_langue_id)
                .first()
            )

            if not cl:
                st.error("❌ Langue introuvable")
                return False

            # Mettre à jour les données
            cl.niveau = data["niveau"]
            cl.niveau_ecrit = data["niveau_ecrit"]
            cl.niveau_parle = data["niveau_parle"]
            cl.certification = data["certification"]
            cl.langue_maternelle = data["langue_maternelle"]

            session.commit()

            return True

    except Exception as e:
        st.error(f"❌ Erreur lors de la mise à jour de la langue: {e}")
        return False


def delete_language(consultant_langue_id: int) -> bool:
    """Supprime une langue du consultant"""

    try:
        with get_database_session() as session:
            cl = (
                session.query(ConsultantLangue)
                .filter(ConsultantLangue.id == consultant_langue_id)
                .first()
            )

            if not cl:
                st.error("❌ Langue introuvable")
                return False

            session.delete(cl)
            session.commit()

            st.info("✅ Langue supprimée")
            return True

    except Exception as e:
        st.error(f"❌ Erreur lors de la suppression de la langue: {e}")
        return False


def show_languages_analysis(consultant_langues):
    """Affiche une analyse des langues"""

    st.markdown("### 📊 Analyse des langues")

    if not consultant_langues:
        st.info("ℹ️ Aucune langue à analyser")
        return

    # Analyse par niveau
    level_counts = {}
    for cl in consultant_langues:
        level = cl.niveau
        level_counts[level] = level_counts.get(level, 0) + 1

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📈 Répartition par niveau")
        for level in range(1, 7):
            count = level_counts.get(level, 0)
            if count > 0:
                st.write(f"**{get_niveau_label(level)} :** {count}")

    with col2:
        st.markdown("#### 🏆 Points forts")
        # Identifier les langues les plus maîtrisées
        best_languages = sorted(
            consultant_langues, key=lambda x: x.niveau, reverse=True
        )[:3]
        for cl in best_languages:
            st.write(f"**{cl.langue.nom} :** {get_niveau_label(cl.niveau)}")

    # Recommandations
    st.markdown("#### 💡 Recommandations")

    # Identifier les langues à améliorer
    weak_languages = [cl for cl in consultant_langues if cl.niveau <= 2]
    if weak_languages:
        st.warning(f"⚠️ **À améliorer :** {len(weak_languages)} langue(s) à renforcer")

    # Langues maternelles
    native_languages = [cl for cl in consultant_langues if cl.langue_maternelle]
    if native_languages:
        st.info(
            f"🏠 **Langues maternelles :** {', '.join([cl.langue.nom for cl in native_languages])}"
        )

    # Certifications
    certified_languages = [cl for cl in consultant_langues if cl.certification]
    if certified_languages:
        st.success(
            f"📜 **Certifications :** {len(certified_languages)} langue(s) certifiée(s)"
        )


def show_languages_comparison(consultant_id: int):
    """Compare les niveaux de langues du consultant avec d'autres consultants"""

    st.markdown("### 🌍 Comparaison des niveaux de langues")

    try:
        with get_database_session() as session:
            # Récupérer les données du consultant
            consultant_languages = (
                session.query(ConsultantLangue)
                .join(Langue)
                .filter(ConsultantLangue.consultant_id == consultant_id)
                .all()
            )

            if not consultant_languages:
                st.info("ℹ️ Aucune langue à comparer")
                return

            # Récupérer les moyennes par langue pour tous les consultants
            from sqlalchemy import func

            language_averages = (
                session.query(
                    Langue.nom,
                    func.avg(ConsultantLangue.niveau).label("avg_level"),
                    func.count(ConsultantLangue.id).label("count"),
                )
                .join(Langue)
                .group_by(Langue.id, Langue.nom)
                .having(func.count(ConsultantLangue.id) > 1)
                .all()
            )

            # Créer un dictionnaire des moyennes
            avg_dict = {
                lang.nom: (lang.avg_level, lang.count) for lang in language_averages
            }

            # Comparer
            comparison_data = []
            for cl in consultant_languages:
                lang_name = cl.langue.nom
                consultant_level = cl.niveau

                if lang_name in avg_dict:
                    avg_level, count = avg_dict[lang_name]
                    difference = consultant_level - avg_level
                    comparison_data.append(
                        {
                            "Langue": lang_name,
                            "Votre niveau": get_niveau_label(consultant_level),
                            "Moyenne équipe": f"{avg_level:.1f}/6",
                            "Écart": f"{difference:+.1f}",
                            "Comparé à": f"{count} consultants",
                        }
                    )

            if comparison_data:
                import pandas as pd

                df = pd.DataFrame(comparison_data)
                st.dataframe(df, use_container_width=True, hide_index=True)

                # Résumé
                above_avg = sum(
                    1 for item in comparison_data if float(item["Écart"]) > 0
                )
                below_avg = sum(
                    1 for item in comparison_data if float(item["Écart"]) < 0
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Au-dessus de la moyenne", above_avg)

                with col2:
                    st.metric("En-dessous de la moyenne", below_avg)
            else:
                st.info("ℹ️ Pas assez de données pour effectuer une comparaison")

    except Exception as e:
        st.error(f"❌ Erreur lors de la comparaison: {e}")
