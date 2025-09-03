"""
Module de gestion des informations personnelles du consultant
Fonctions pour afficher et modifier les informations de base
"""

import os
import sys
from datetime import datetime
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
imports_ok = False

try:
    from app.database.database import get_database_session
    from app.database.models import Consultant, ConsultantSalaire, ConsultantCompetence, Mission
    from app.services.consultant_service import ConsultantService

    imports_ok = True
except ImportError as e:
    # Imports échoués, on continue quand même
    pass


def show_consultant_info(consultant):
    """Affiche les informations personnelles du consultant"""

    if not imports_ok:
        st.error("❌ Les services de base ne sont pas disponibles")
        return

    if not consultant:
        st.error("❌ Consultant non fourni")
        return

    st.markdown("### 📋 Informations personnelles")

    try:
        # Informations de base
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 👤 Identité")
            st.write(f"**Prénom :** {consultant.prenom}")
            st.write(f"**Nom :** {consultant.nom}")
            st.write(f"**Email :** {consultant.email}")

            if consultant.telephone:
                st.write(f"**Téléphone :** {consultant.telephone}")

        with col2:
            st.markdown("#### 🏢 Affectation")
            practice_name = consultant.practice.nom if consultant.practice else "Non affecté"
            st.write(f"**Practice :** {practice_name}")

            status = "✅ Disponible" if consultant.disponibilite else "🔴 En mission"
            st.write(f"**Statut :** {status}")

            if consultant.date_creation:
                st.write(f"**Membre depuis :** {consultant.date_creation.strftime('%d/%m/%Y')}")

        # Informations financières
        st.markdown("#### 💰 Informations financières")

        col1, col2, col3 = st.columns(3)

        with col1:
            salaire = consultant.salaire_actuel or 0
            st.metric("Salaire annuel", f"{salaire:,}€")

        with col2:
            # Calcul du CJM (Coût Journalier Moyen)
            cjm = (salaire * 1.8 / 216) if salaire else 0
            st.metric("CJM estimé", f"{cjm:,.0f}€")

        with col3:
            # Calcul du TJM (Taux Journalier Moyen)
            tjm = (salaire * 1.5 / 216) if salaire else 0
            st.metric("TJM estimé", f"{tjm:,.0f}€")

        # Historique des salaires
        show_salary_history(consultant.id)

        # Notes
        if consultant.notes:
            st.markdown("#### 📝 Notes")
            st.text_area(
                "Notes du consultant",
                value=consultant.notes,
                height=100,
                disabled=True,
                key=f"notes_{consultant.id}"
            )

        # Actions
        st.markdown("#### 🎯 Actions")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("✏️ Modifier", key=f"edit_info_{consultant.id}"):
                st.session_state.edit_consultant_info = consultant.id
                st.rerun()

        with col2:
            if st.button("💰 Historique salaire", key=f"salary_history_{consultant.id}"):
                st.session_state.show_salary_history = consultant.id
                st.rerun()

        with col3:
            if st.button("📊 Générer rapport", key=f"generate_report_{consultant.id}"):
                generate_consultant_report(consultant)

        # Formulaire de modification (si activé)
        if "edit_consultant_info" in st.session_state and st.session_state.edit_consultant_info == consultant.id:
            show_edit_info_form(consultant)

        # Historique détaillé des salaires (si activé)
        if "show_salary_history" in st.session_state and st.session_state.show_salary_history == consultant.id:
            show_detailed_salary_history(consultant.id)

    except Exception as e:
        st.error(f"❌ Erreur lors de l'affichage des informations: {e}")
        st.code(str(e))


def show_salary_history(consultant_id: int):
    """Affiche un aperçu de l'historique des salaires"""

    try:
        with get_database_session() as session:
            salaries = session.query(ConsultantSalaire)\
                .filter(ConsultantSalaire.consultant_id == consultant_id)\
                .order_by(ConsultantSalaire.date_debut.desc())\
                .limit(5)\
                .all()

        if salaries:
            st.markdown("#### 📈 Évolution salariale récente")

            # Créer un tableau simple
            salary_data = []
            for salary in salaries:
                salary_data.append({
                    'Date': salary.date_debut.strftime('%d/%m/%Y'),
                    'Salaire': f"{salary.salaire:,}€",
                    'Motif': salary.commentaire or "N/A"
                })

            import pandas as pd
            df = pd.DataFrame(salary_data)
            st.dataframe(df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.warning(f"⚠️ Impossible de charger l'historique des salaires: {e}")


def show_detailed_salary_history(consultant_id: int):
    """Affiche l'historique détaillé des salaires"""

    st.markdown("### 📈 Historique salarial détaillé")

    try:
        with get_database_session() as session:
            salaries = session.query(ConsultantSalaire)\
                .filter(ConsultantSalaire.consultant_id == consultant_id)\
                .order_by(ConsultantSalaire.date_debut.desc())\
                .all()

        if not salaries:
            st.info("ℹ️ Aucun historique salarial trouvé")
            return

        # Statistiques
        col1, col2, col3 = st.columns(3)

        with col1:
            current_salary = salaries[0].salaire if salaries else 0
            st.metric("Salaire actuel", f"{current_salary:,}€")

        with col2:
            min_salary = min(s.salaire for s in salaries) if salaries else 0
            st.metric("Salaire minimum", f"{min_salary:,}€")

        with col3:
            max_salary = max(s.salaire for s in salaries) if salaries else 0
            st.metric("Salaire maximum", f"{max_salary:,}€")

        # Tableau détaillé
        salary_data = []
        for salary in salaries:
            salary_data.append({
                'Date': salary.date_debut.strftime('%d/%m/%Y'),
                'Salaire': salary.salaire,
                'Motif': salary.commentaire or "N/A",
                'Évolution': "N/A"  # Sera calculé après
            })

        # Calculer les évolutions
        for i in range(len(salary_data) - 1):
            current = salary_data[i]['Salaire']
            previous = salary_data[i + 1]['Salaire']
            evolution = ((current - previous) / previous) * 100 if previous > 0 else 0
            salary_data[i]['Évolution'] = f"{evolution:+.1f}%"

        import pandas as pd
        df = pd.DataFrame(salary_data)

        # Formater les colonnes
        df['Salaire'] = df['Salaire'].apply(lambda x: f"{x:,}€")

        st.dataframe(df, use_container_width=True, hide_index=True)

        # Bouton pour fermer
        if st.button("❌ Fermer l'historique", key="close_salary_history"):
            del st.session_state.show_salary_history
            st.rerun()

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement de l'historique détaillé: {e}")


def show_edit_info_form(consultant):
    """Affiche le formulaire de modification des informations"""

    st.markdown("### ✏️ Modifier les informations")

    with st.form(f"edit_info_form_{consultant.id}", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            prenom = st.text_input("Prénom *", value=consultant.prenom)
            email = st.text_input("Email *", value=consultant.email)
            telephone = st.text_input("Téléphone", value=consultant.telephone or "")

        with col2:
            nom = st.text_input("Nom *", value=consultant.nom)
            salaire_actuel = st.number_input(
                "Salaire annuel (€)",
                value=consultant.salaire_actuel or 0,
                min_value=0,
                step=1000
            )
            motif_changement = st.text_input(
                "Commentaire du changement de salaire",
                placeholder="Ex: Augmentation annuelle, Promotion..."
            )

        disponibilite = st.checkbox("Disponible", value=consultant.disponibilite)
        notes = st.text_area("Notes", value=consultant.notes or "", height=100)

        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            submitted = st.form_submit_button("💾 Enregistrer", type="primary")

        with col2:
            cancel = st.form_submit_button("❌ Annuler")

        with col3:
            pass

        if submitted:
            if validate_info_form(prenom, nom, email):
                success = update_consultant_info(consultant.id, {
                    'prenom': prenom,
                    'nom': nom,
                    'email': email,
                    'telephone': telephone,
                    'salaire_actuel': salaire_actuel,
                    'disponibilite': disponibilite,
                    'notes': notes,
                    'commentaire': motif_changement
                })

                if success:
                    st.success("✅ Informations mises à jour !")
                    del st.session_state.edit_consultant_info
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de la mise à jour")
            else:
                st.error("❌ Veuillez corriger les erreurs")

        if cancel:
            del st.session_state.edit_consultant_info
            st.rerun()


def validate_info_form(prenom: str, nom: str, email: str) -> bool:
    """Valide les données du formulaire d'informations"""

    errors = []

    if not prenom or not prenom.strip():
        errors.append("Le prénom est obligatoire")

    if not nom or not nom.strip():
        errors.append("Le nom est obligatoire")

    if not email or not email.strip():
        errors.append("L'email est obligatoire")
    elif "@" not in email:
        errors.append("L'email doit être valide")

    if errors:
        for error in errors:
            st.error(f"❌ {error}")
        return False

    return True


def update_consultant_info(consultant_id: int, data: dict) -> bool:
    """Met à jour les informations du consultant"""

    try:
        with get_database_session() as session:
            consultant = session.query(Consultant).filter(Consultant.id == consultant_id).first()

            if not consultant:
                st.error("❌ Consultant introuvable")
                return False

            # Vérifier l'unicité de l'email
            existing = session.query(Consultant)\
                .filter(Consultant.email == data['email'], Consultant.id != consultant_id)\
                .first()
            if existing:
                st.error("❌ Cet email est déjà utilisé par un autre consultant")
                return False

            # Sauvegarder l'ancien salaire si changé
            old_salary = consultant.salaire_actuel
            new_salary = data['salaire_actuel']

            if old_salary != new_salary and data.get('commentaire'):
                salary_history = ConsultantSalaire(
                    consultant_id=consultant_id,
                    salaire=old_salary,
                    date_debut=datetime.now(),
                    commentaire=data['commentaire']
                )
                session.add(salary_history)

            # Mettre à jour les informations
            consultant.prenom = data['prenom'].strip()
            consultant.nom = data['nom'].strip()
            consultant.email = data['email'].strip().lower()
            consultant.telephone = data['telephone'].strip() if data['telephone'] else None
            consultant.salaire_actuel = new_salary
            consultant.disponibilite = data['disponibilite']
            consultant.notes = data['notes'].strip() if data['notes'] else None

            session.commit()

            st.info("✅ Informations du consultant mises à jour")
            return True

    except Exception as e:
        st.error(f"❌ Erreur lors de la mise à jour: {e}")
        return False


def generate_consultant_report(consultant):
    """Génère un rapport simple du consultant"""

    try:
        st.markdown("### 📊 Rapport du consultant")

        # Informations de base
        st.write(f"**Nom complet :** {consultant.prenom} {consultant.nom}")
        st.write(f"**Email :** {consultant.email}")
        st.write(f"**Practice :** {consultant.practice.nom if consultant.practice else 'Non affecté'}")
        st.write(f"**Statut :** {'Disponible' if consultant.disponibilite else 'En mission'}")

        # Informations financières
        salaire = consultant.salaire_actuel or 0
        st.write(f"**Salaire annuel :** {salaire:,}€")
        cjm = (salaire * 1.8 / 216) if salaire else 0
        st.write(f"**CJM estimé :** {cjm:,.0f}€")

        # Statistiques des compétences (si disponibles)
        try:
            with get_database_session() as session:
                competence_count = session.query(ConsultantCompetence)\
                    .filter(ConsultantCompetence.consultant_id == consultant.id)\
                    .count()

                mission_count = session.query(Mission)\
                    .filter(Mission.consultant_id == consultant.id)\
                    .count()

            st.write(f"**Nombre de compétences :** {competence_count}")
            st.write(f"**Nombre de missions :** {mission_count}")

        except Exception as e:
            st.warning(f"⚠️ Impossible de charger les statistiques: {e}")

        st.success("✅ Rapport généré avec succès !")

    except Exception as e:
        st.error(f"❌ Erreur lors de la génération du rapport: {e}")
