"""
Module de gestion des formulaires consultants
Fonctions pour ajouter et modifier les consultants
"""

import os
import sys
from datetime import datetime
from typing import Any
from typing import Dict
from typing import Optional

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
Practice = None
imports_ok = False

try:
    from sqlalchemy.orm import joinedload

    from database.database import get_database_session
    from database.models import Competence
    from database.models import Consultant
    from database.models import ConsultantCompetence
    from database.models import ConsultantLangue
    from database.models import Langue
    from database.models import Practice
    from services.consultant_service import ConsultantService

    imports_ok = True
except ImportError as e:
    # Imports échoués, on continue quand même
    pass


def show_add_consultant_form():
    """Affiche le formulaire d'ajout d'un nouveau consultant"""

    if not imports_ok:
        st.error("❌ Les services de base ne sont pas disponibles")
        return

    st.markdown("### ➕ Ajouter un nouveau consultant")

    # Récupérer les practices disponibles
    try:
        with get_database_session() as session:
            practices = session.query(Practice).all()
            practice_options = {p.id: p.nom for p in practices}

        if not practice_options:
            st.warning(
                "⚠️ Aucune practice trouvée. Veuillez créer des practices d'abord."
            )
            return

        with st.form("add_consultant_form", clear_on_submit=True):
            st.markdown("#### 📋 Informations personnelles")

            col1, col2 = st.columns(2)

            with col1:
                prenom = st.text_input("Prénom *", help="Prénom du consultant")

                email = st.text_input("Email *", help="Adresse email professionnelle")

                salaire_actuel = st.number_input(
                    "Salaire annuel (€)",
                    min_value=0,
                    step=1000,
                    help="Salaire annuel brut en euros",
                )

            with col2:
                nom = st.text_input("Nom *", help="Nom de famille du consultant")

                telephone = st.text_input(
                    "Téléphone", help="Numéro de téléphone professionnel"
                )

                practice_id = st.selectbox(
                    "Practice *",
                    options=list(practice_options.keys()),
                    format_func=lambda x: practice_options[x],
                    help="Practice d'affectation",
                )

            st.markdown("#### 📝 Informations complémentaires")

            disponibilite = st.checkbox(
                "Disponible pour de nouvelles missions",
                value=True,
                help="Cochez si le consultant est disponible",
            )

            notes = st.text_area(
                "Notes",
                height=100,
                help="Informations complémentaires sur le consultant",
            )

            # Boutons du formulaire
            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                submitted = st.form_submit_button("💾 Enregistrer", type="primary")

            with col2:
                reset = st.form_submit_button("🔄 Réinitialiser")

            with col3:
                cancel = st.form_submit_button("❌ Annuler")

            # Traitement du formulaire
            if submitted:
                if validate_consultant_form(prenom, nom, email, practice_id):
                    success = create_consultant(
                        {
                            "prenom": prenom,
                            "nom": nom,
                            "email": email,
                            "telephone": telephone,
                            "salaire_actuel": salaire_actuel,
                            "practice_id": practice_id,
                            "disponibilite": disponibilite,
                            "notes": notes,
                        }
                    )

                    if success:
                        st.success("✅ Consultant ajouté avec succès !")
                        st.balloons()
                        # Recharger la page pour afficher le nouveau consultant
                        st.rerun()
                    else:
                        st.error("❌ Erreur lors de l'ajout du consultant")
                else:
                    st.error("❌ Veuillez corriger les erreurs ci-dessus")

            if reset:
                st.rerun()

            if cancel:
                st.info("ℹ️ Ajout annulé")

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du formulaire: {e}")
        st.code(str(e))


def validate_consultant_form(
    prenom: str, nom: str, email: str, practice_id: int
) -> bool:
    """Valide les données du formulaire consultant"""

    errors = []

    if not prenom or not prenom.strip():
        errors.append("Le prénom est obligatoire")

    if not nom or not nom.strip():
        errors.append("Le nom est obligatoire")

    if not email or not email.strip():
        errors.append("L'email est obligatoire")
    elif "@" not in email:
        errors.append("L'email doit être valide")

    if not practice_id:
        errors.append("La practice est obligatoire")

    if errors:
        for error in errors:
            st.error(f"❌ {error}")
        return False

    return True


def create_consultant(data: Dict[str, Any]) -> bool:
    """Crée un nouveau consultant dans la base de données"""

    try:
        with get_database_session() as session:
            # Vérifier si l'email existe déjà
            existing = (
                session.query(Consultant)
                .filter(Consultant.email == data["email"])
                .first()
            )
            if existing:
                st.error("❌ Un consultant avec cet email existe déjà")
                return False

            # Créer le consultant
            consultant = Consultant(
                prenom=data["prenom"].strip(),
                nom=data["nom"].strip(),
                email=data["email"].strip().lower(),
                telephone=data["telephone"].strip() if data["telephone"] else None,
                salaire_actuel=data["salaire_actuel"],
                practice_id=data["practice_id"],
                disponibilite=data["disponibilite"],
                notes=data["notes"].strip() if data["notes"] else None,
                date_creation=datetime.now(),
            )

            session.add(consultant)
            session.commit()

            st.info(
                f"✅ Consultant {
                    consultant.prenom} {
                    consultant.nom} créé avec l'ID {
                    consultant.id}"
            )
            return True

    except Exception as e:
        st.error(f"❌ Erreur lors de la création du consultant: {e}")
        return False


def show_edit_consultant_form(consultant_id: int):
    """Affiche le formulaire de modification d'un consultant"""

    if not imports_ok:
        st.error("❌ Les services de base ne sont pas disponibles")
        return

    try:
        # Charger le consultant
        with get_database_session() as session:
            consultant = (
                session.query(Consultant)
                .options(joinedload(Consultant.practice))
                .filter(Consultant.id == consultant_id)
                .first()
            )

            if not consultant:
                st.error("❌ Consultant introuvable")
                return

            # Récupérer les practices
            practices = session.query(Practice).all()
            practice_options = {p.id: p.nom for p in practices}

        st.markdown(f"### ✏️ Modifier {consultant.prenom} {consultant.nom}")

        with st.form(f"edit_consultant_form_{consultant_id}", clear_on_submit=False):
            st.markdown("#### 📋 Informations personnelles")

            col1, col2 = st.columns(2)

            with col1:
                prenom = st.text_input(
                    "Prénom *", value=consultant.prenom, help="Prénom du consultant"
                )

                email = st.text_input(
                    "Email *",
                    value=consultant.email,
                    help="Adresse email professionnelle",
                )

                salaire_actuel = st.number_input(
                    "Salaire annuel (€)",
                    value=consultant.salaire_actuel or 0,
                    min_value=0,
                    step=1000,
                    help="Salaire annuel brut en euros",
                )

            with col2:
                nom = st.text_input(
                    "Nom *", value=consultant.nom, help="Nom de famille du consultant"
                )

                telephone = st.text_input(
                    "Téléphone",
                    value=consultant.telephone or "",
                    help="Numéro de téléphone professionnel",
                )

                practice_id = st.selectbox(
                    "Practice *",
                    options=list(practice_options.keys()),
                    format_func=lambda x: practice_options[x],
                    index=(
                        list(practice_options.keys()).index(consultant.practice_id)
                        if consultant.practice_id in practice_options
                        else 0
                    ),
                    help="Practice d'affectation",
                )

            st.markdown("#### 📝 Informations complémentaires")

            disponibilite = st.checkbox(
                "Disponible pour de nouvelles missions",
                value=consultant.disponibilite,
                help="Cochez si le consultant est disponible",
            )

            notes = st.text_area(
                "Notes",
                value=consultant.notes or "",
                height=100,
                help="Informations complémentaires sur le consultant",
            )

            # Boutons du formulaire
            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                submitted = st.form_submit_button("💾 Enregistrer", type="primary")

            with col2:
                delete = st.form_submit_button("🗑️ Supprimer", type="secondary")

            with col3:
                cancel = st.form_submit_button("❌ Annuler")

            # Traitement du formulaire
            if submitted:
                if validate_consultant_form(prenom, nom, email, practice_id):
                    success = update_consultant(
                        consultant_id,
                        {
                            "prenom": prenom,
                            "nom": nom,
                            "email": email,
                            "telephone": telephone,
                            "salaire_actuel": salaire_actuel,
                            "practice_id": practice_id,
                            "disponibilite": disponibilite,
                            "notes": notes,
                        },
                    )

                    if success:
                        st.success("✅ Consultant modifié avec succès !")
                        st.rerun()
                    else:
                        st.error("❌ Erreur lors de la modification du consultant")
                else:
                    st.error("❌ Veuillez corriger les erreurs ci-dessus")

            if delete:
                st.warning("⚠️ Cette action est irréversible !")
                if st.checkbox("Je confirme vouloir supprimer ce consultant"):
                    if delete_consultant(consultant_id):
                        st.success("✅ Consultant supprimé avec succès !")
                        # Retourner à la liste
                        if "view_consultant_profile" in st.session_state:
                            del st.session_state.view_consultant_profile
                        st.rerun()

            if cancel:
                st.info("ℹ️ Modification annulée")

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du formulaire de modification: {e}")
        st.code(str(e))


def update_consultant(consultant_id: int, data: Dict[str, Any]) -> bool:
    """Met à jour un consultant dans la base de données"""

    try:
        with get_database_session() as session:
            consultant = (
                session.query(Consultant).filter(Consultant.id == consultant_id).first()
            )

            if not consultant:
                st.error("❌ Consultant introuvable")
                return False

            # Vérifier si l'email existe déjà pour un autre consultant
            existing = (
                session.query(Consultant)
                .filter(
                    Consultant.email == data["email"], Consultant.id != consultant_id
                )
                .first()
            )
            if existing:
                st.error("❌ Un autre consultant utilise déjà cet email")
                return False

            # Mettre à jour les données
            consultant.prenom = data["prenom"].strip()
            consultant.nom = data["nom"].strip()
            consultant.email = data["email"].strip().lower()
            consultant.telephone = (
                data["telephone"].strip() if data["telephone"] else None
            )
            consultant.salaire_actuel = data["salaire_actuel"]
            consultant.practice_id = data["practice_id"]
            consultant.disponibilite = data["disponibilite"]
            consultant.notes = data["notes"].strip() if data["notes"] else None

            session.commit()

            st.info(f"✅ Consultant {consultant.prenom} {consultant.nom} modifié")
            return True

    except Exception as e:
        st.error(f"❌ Erreur lors de la modification du consultant: {e}")
        return False


def delete_consultant(consultant_id: int) -> bool:
    """Supprime un consultant de la base de données"""

    try:
        with get_database_session() as session:
            consultant = (
                session.query(Consultant).filter(Consultant.id == consultant_id).first()
            )

            if not consultant:
                st.error("❌ Consultant introuvable")
                return False

            # Supprimer le consultant (les relations seront supprimées automatiquement
            # grâce aux cascades)
            session.delete(consultant)
            session.commit()

            st.info("✅ Consultant supprimé de la base de données")
            return True

    except Exception as e:
        st.error(f"❌ Erreur lors de la suppression du consultant: {e}")
        return False
