"""
Module de gestion des informations personnelles du consultant
Fonctions pour afficher et modifier les informations de base
"""

import os
import sys
from datetime import datetime
from typing import Optional

import streamlit as st

# Constantes pour les messages
MSG_SERVICES_INDISPONIBLES = "❌ Les services de base ne sont pas disponibles"
MSG_CONSULTANT_NON_FOURNI = "❌ Consultant non fourni"
MSG_ERREUR_AFFICHAGE = "❌ Erreur lors de l'affichage des informations"
MSG_ERREUR_HISTORIQUE = "⚠️ Impossible de charger l'historique des salaires"
MSG_ERREUR_HISTORIQUE_DETAILLE = "❌ Erreur lors du chargement de l'historique détaillé"
MSG_ERREUR_MODIFICATION = "❌ Erreur lors de la modification"
MSG_ERREUR_RAPPORT = "❌ Erreur lors de la génération du rapport"
MSG_ERREUR_MISE_A_JOUR = "❌ Erreur lors de la mise à jour"
MSG_AUCUN_HISTORIQUE = "ℹ️ Aucun historique salarial trouvé"
MSG_SUCCESS_MODIFICATION = "✅ Informations mises à jour avec succès !"

# Constantes pour les statuts
STATUS_DISPONIBLE = "✅ Disponible"
STATUS_EN_MISSION = "🔴 En mission"
DEFAULT_PRACTICE = "Non affecté"
DEFAULT_VALUE = "N/A"

# Constantes pour les calculs financiers
COEFF_CJM = 1.8
COEFF_TJM = 1.5
JOURS_TRAVAIL_ANNUEL = 216

# Constantes pour l'affichage des dates
DATE_FORMAT = "%d/%m/%Y"

# Ajouter les chemins nécessaires
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


def _calculate_availability_status(consultant) -> str:
    """
    Calcule le statut de disponibilité basé sur les missions du consultant

    Args:
        consultant: Objet Consultant avec ses missions

    Returns:
        str: Statut de disponibilité formaté
    """
    if not consultant.missions:
        return STATUS_DISPONIBLE

    # Trouver la mission avec la date de fin la plus récente (future)
    today = datetime.now().date()
    latest_end_date = None

    for mission in consultant.missions:
        if mission.date_fin and mission.date_fin >= today:
            if latest_end_date is None or mission.date_fin > latest_end_date:
                latest_end_date = mission.date_fin

    # Si aucune mission future trouvée, le consultant est disponible
    if latest_end_date is None:
        return STATUS_DISPONIBLE

    # Calculer les jours jusqu'à la fin de la mission
    days_until_available = (latest_end_date - today).days

    if days_until_available <= 0:
        return STATUS_DISPONIBLE
    elif days_until_available <= 90:
        return f"⏳ Disponible dans {days_until_available} jours"
    else:
        return "❌ Non disponible"


# Variables pour les imports
ConsultantService = None
get_database_session = None
Consultant = None
imports_ok = False

try:
    from database.database import get_database_session
    from database.models import Consultant, ConsultantCompetence, ConsultantSalaire, Mission
    from services.consultant_service import ConsultantService

    imports_ok = True
except ImportError:
    # Imports échoués, on continue quand même
    pass


def _display_identity_info(consultant) -> None:
    """Affiche les informations d'identité du consultant"""
    st.markdown("#### 👤 Identité")
    st.write(f"**Prénom :** {consultant.prenom}")
    st.write(f"**Nom :** {consultant.nom}")
    st.write(f"**Email :** {consultant.email}")

    if consultant.telephone:
        st.write(f"**Téléphone :** {consultant.telephone}")


def _display_affectation_info(consultant) -> None:
    """Affiche les informations d'affectation du consultant"""
    st.markdown("#### 🏢 Affectation")
    practice_name = consultant.practice.nom if consultant.practice else DEFAULT_PRACTICE
    st.write(f"**Practice :** {practice_name}")
    st.write(f"**Entité :** {consultant.entite or 'N/A'}")

    # Informations contractuelles avec période d'essai
    col1, col2 = st.columns(2)
    with col1:
        type_contrat = getattr(consultant, "type_contrat", "N/A")
        st.write(f"**Type de contrat :** {type_contrat}")
    with col2:
        etat_pe = getattr(consultant, "etat_periode_essai", None)
        if etat_pe:
            st.write(f"**Période d'essai :** {etat_pe}")
        else:
            st.write("**Période d'essai :** N/A")

    # Date fin période d'essai si elle existe
    fin_pe = getattr(consultant, "fin_periode_essai", None)
    if fin_pe:
        st.write(f"**Fin période d'essai :** {fin_pe.strftime(DATE_FORMAT)}")

    # Statuts
    col3, col4 = st.columns(2)
    with col3:
        status = _calculate_availability_status(consultant)
        st.write(f"**Disponibilité :** {status}")
    with col4:
        actif = getattr(consultant, "actif", True)
        statut_actif = "✅ Actif" if actif else "❌ Inactif"
        st.write(f"**Statut :** {statut_actif}")

    # Statut société
    try:
        statut_soc = consultant.statut_societe
        if statut_soc == "En poste":
            st.success(f"✅ **Statut société :** {statut_soc}")
        elif statut_soc == "Départ prévu":
            st.warning(f"⚠️ **Statut société :** {statut_soc}")
        else:
            st.error(f"❌ **Statut société :** {statut_soc}")
    except (AttributeError, TypeError, ValueError):
        st.info("📊 **Statut société :** En cours de calcul...")

    if consultant.date_creation:
        st.write(f"**Membre depuis :** {consultant.date_creation.strftime(DATE_FORMAT)}")


def _display_financial_info(consultant) -> None:
    """Affiche les informations financières du consultant"""
    st.markdown("#### 💰 Informations financières")

    col1, col2, col3 = st.columns(3)

    with col1:
        salaire = consultant.salaire_actuel or 0
        st.metric("Salaire annuel", f"{salaire:,}€")

    with col2:
        # Calcul du CJM (Coût Journalier Moyen)
        cjm = (salaire * COEFF_CJM / JOURS_TRAVAIL_ANNUEL) if salaire else 0
        st.metric("CJM estimé", f"{cjm:,.0f}€")

    with col3:
        # Calcul du TJM (Taux Journalier Moyen)
        tjm = (salaire * COEFF_TJM / JOURS_TRAVAIL_ANNUEL) if salaire else 0
        st.metric("TJM estimé", f"{tjm:,.0f}€")


def _display_notes_section(consultant) -> None:
    """Affiche la section des notes du consultant"""
    if consultant.notes:
        st.markdown("#### 📝 Notes")
        st.text_area(
            "Notes du consultant",
            value=consultant.notes,
            height=100,
            disabled=True,
            key=f"notes_{consultant.id}",
        )


# Constantes pour l'affichage des missions VSA
COL_CODE = "Code"
COL_ORDERID = "N° Commande"
COL_CLIENT = "Client"
COL_DATE_DEBUT = "Date début"
COL_DATE_FIN = "Date fin"
COL_TJM = "TJM"
COL_CJM = "CJM"
COL_STATUT = "Statut"
COL_DUREE = "Durée"
NA_VALUE = "N/A"


def _display_vsa_missions(consultant) -> None:
    """Affiche les missions VSA du consultant"""
    st.markdown("#### 🎯 Missions VSA")

    # Checkbox pour filtrer la facturation interne
    # Par défaut, décoché = affiche les missions qui ne commencent pas par INT
    # Si coché = affiche seulement les missions qui commencent par INT

    # Utiliser l'ID du consultant pour une clé unique et stable
    checkbox_key = f"vsa_internal_checkbox_{consultant.id}"

    facturation_interne = st.checkbox(
        "Facturation interne",
        key=checkbox_key,
        help="Coché: affiche seulement les missions internes (codes INT*). Décoché: affiche les missions externes (codes non INT*)",
    )

    try:
        with get_database_session() as session:
            # Importer VsaMission ici pour éviter les dépendances circulaires
            from database.models import VsaMission

            missions_vsa = (
                session.query(VsaMission)
                .filter(VsaMission.user_id == consultant.id)
                .order_by(VsaMission.date_debut.desc())
                .all()
            )

        if not missions_vsa:
            st.info("ℹ️ Aucune mission VSA trouvée pour ce consultant")
            return

        # Filtrage des missions selon la checkbox
        if facturation_interne:
            # Afficher seulement les missions internes (codes commençant par INT)
            missions_filtrees = [m for m in missions_vsa if m.code.startswith("INT")]
            filter_info = "🏢 Missions de facturation interne (INT*)"
        else:
            # Afficher seulement les missions externes (codes ne commençant pas par INT)
            missions_filtrees = [m for m in missions_vsa if not m.code.startswith("INT")]
            filter_info = "🌍 Missions externes (hors INT*)"

        # Affichage du filtre actuel
        st.info(f"{filter_info} - {len(missions_filtrees)} mission(s) sur {len(missions_vsa)} total")

        if not missions_filtrees:
            type_missions = "internes" if facturation_interne else "externes"
            st.warning(f"ℹ️ Aucune mission {type_missions} trouvée pour ce consultant")
            return

        # Statistiques des missions VSA filtrées
        _display_vsa_missions_stats(missions_filtrees)

        # Tableau des missions VSA filtrées
        _display_vsa_missions_table(missions_filtrees, consultant)

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des missions VSA: {e}")
        st.code(str(e))


def _display_vsa_missions_stats(missions_vsa) -> None:
    """Affiche les statistiques des missions VSA"""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🎯 Total missions VSA", len(missions_vsa))

    with col2:
        active_missions = sum(1 for m in missions_vsa if m.est_active)
        st.metric("✅ Missions actives", active_missions)

    with col3:
        missions_with_tjm = [m for m in missions_vsa if m.tjm]
        avg_tjm = sum(m.tjm for m in missions_with_tjm) / len(missions_with_tjm) if missions_with_tjm else 0
        st.metric("💰 TJM moyen", f"{avg_tjm:,.0f}€")


def _display_vsa_missions_table(missions_vsa, consultant) -> None:
    """Affiche le tableau des missions VSA"""
    missions_data = []
    for mission in missions_vsa:
        missions_data.append(
            {
                COL_CODE: mission.code,
                COL_ORDERID: mission.orderid,
                COL_CLIENT: mission.client_name,
                COL_DATE_DEBUT: (mission.date_debut.strftime(DATE_FORMAT) if mission.date_debut else NA_VALUE),
                COL_DATE_FIN: (mission.date_fin.strftime(DATE_FORMAT) if mission.date_fin else NA_VALUE),
                COL_TJM: f"{mission.tjm:,.0f}€" if mission.tjm else NA_VALUE,
                COL_CJM: f"{mission.cjm:,.0f}€" if mission.cjm else NA_VALUE,
                COL_STATUT: "✅ Active" if mission.est_active else "❌ Terminée",
                COL_DUREE: (f"{mission.duree_jours} jours" if mission.duree_jours else NA_VALUE),
            }
        )

    import pandas as pd

    df = pd.DataFrame(missions_data)

    # Configuration des colonnes
    column_config = {
        COL_CODE: st.column_config.TextColumn(COL_CODE, width="small"),
        COL_ORDERID: st.column_config.TextColumn(COL_ORDERID, width="medium"),
        COL_CLIENT: st.column_config.TextColumn(COL_CLIENT, width="large"),
        COL_DATE_DEBUT: st.column_config.TextColumn(COL_DATE_DEBUT, width="small"),
        COL_DATE_FIN: st.column_config.TextColumn(COL_DATE_FIN, width="small"),
        COL_TJM: st.column_config.TextColumn(COL_TJM, width="small"),
        COL_CJM: st.column_config.TextColumn(COL_CJM, width="small"),
        COL_STATUT: st.column_config.TextColumn(COL_STATUT, width="small"),
        COL_DUREE: st.column_config.TextColumn(COL_DUREE, width="small"),
    }

    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
        column_config=column_config,
    )

    # Bouton pour rafraîchir
    if st.button("🔄 Actualiser les missions VSA", key=f"refresh_vsa_{consultant.id}"):
        st.rerun()


def _display_action_buttons(consultant) -> None:
    """Affiche les boutons d'actions pour le consultant"""
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


def _handle_conditional_displays(consultant) -> None:
    """Gère l'affichage conditionnel des formulaires et historiques"""
    # Formulaire de modification (si activé)
    if "edit_consultant_info" in st.session_state and st.session_state.edit_consultant_info == consultant.id:
        show_edit_info_form(consultant)

    # Historique détaillé des salaires (si activé)
    if "show_salary_history" in st.session_state and st.session_state.show_salary_history == consultant.id:
        show_detailed_salary_history(consultant.id)


def show_consultant_info(consultant):
    """Affiche les informations personnelles du consultant"""

    if not imports_ok:
        st.error(MSG_SERVICES_INDISPONIBLES)
        return

    if not consultant:
        st.error(MSG_CONSULTANT_NON_FOURNI)
        return

    try:
        # Informations de base
        col1, col2 = st.columns(2)

        with col1:
            _display_identity_info(consultant)

        with col2:
            _display_affectation_info(consultant)

        # Informations financières
        _display_financial_info(consultant)

        # Historique des salaires
        show_salary_history(consultant.id)

        # Notes
        _display_notes_section(consultant)

        # Actions
        _display_action_buttons(consultant)

        # Gestion des affichages conditionnels
        _handle_conditional_displays(consultant)

    except Exception as e:
        st.error(f"{MSG_ERREUR_AFFICHAGE}: {e}")
        st.code(str(e))


def show_salary_history(consultant_id: int):
    """Affiche un aperçu de l'historique des salaires"""

    try:
        with get_database_session() as session:
            salaries = (
                session.query(ConsultantSalaire)
                .filter(ConsultantSalaire.consultant_id == consultant_id)
                .order_by(ConsultantSalaire.date_debut.desc())
                .limit(5)
                .all()
            )

        if salaries:
            st.markdown("#### 📈 Évolution salariale récente")

            # Créer un tableau simple
            salary_data = []
            for salary in salaries:
                salary_data.append(
                    {
                        "Date": salary.date_debut.strftime(DATE_FORMAT),
                        "Salaire": f"{salary.salaire:,}€",
                        "Motif": salary.commentaire or DEFAULT_VALUE,
                    }
                )

            import pandas as pd

            df = pd.DataFrame(salary_data)
            st.dataframe(df, width="stretch", hide_index=True)

    except Exception as e:
        st.warning(f"{MSG_ERREUR_HISTORIQUE}: {e}")


def show_detailed_salary_history(consultant_id: int):
    """Affiche l'historique détaillé des salaires"""

    st.markdown("### 📈 Historique salarial détaillé")

    try:
        with get_database_session() as session:
            salaries = (
                session.query(ConsultantSalaire)
                .filter(ConsultantSalaire.consultant_id == consultant_id)
                .order_by(ConsultantSalaire.date_debut.desc())
                .all()
            )

        if not salaries:
            st.info(MSG_AUCUN_HISTORIQUE)
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
            salary_data.append(
                {
                    "Date": salary.date_debut.strftime(DATE_FORMAT),
                    "Salaire": salary.salaire,
                    "Motif": salary.commentaire or DEFAULT_VALUE,
                    "Évolution": DEFAULT_VALUE,  # Sera calculé après
                }
            )

        # Calculer les évolutions
        for i in range(len(salary_data) - 1):
            current = salary_data[i]["Salaire"]
            previous = salary_data[i + 1]["Salaire"]
            evolution = ((current - previous) / previous) * 100 if previous > 0 else 0
            salary_data[i]["Évolution"] = f"{evolution:+.1f}%"

        import pandas as pd

        df = pd.DataFrame(salary_data)

        # Formater les colonnes
        df["Salaire"] = df["Salaire"].apply(lambda x: f"{x:,}€")

        st.dataframe(df, width="stretch", hide_index=True)

        # Bouton pour fermer
        if st.button("❌ Fermer l'historique", key="close_salary_history"):
            del st.session_state.show_salary_history
            st.rerun()

    except Exception as e:
        st.error(f"{MSG_ERREUR_HISTORIQUE_DETAILLE}: {e}")


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
                step=1000,
            )
            motif_changement = st.text_input(
                "Commentaire du changement de salaire",
                placeholder="Ex: Augmentation annuelle, Promotion...",
            )

        disponibilite = st.checkbox("Disponible", value=consultant.disponibilite)
        notes = st.text_area("Notes", value=consultant.notes or "", height=100)

        col1, col2 = st.columns(2)

        with col1:
            submitted = st.form_submit_button("💾 Enregistrer", type="primary")

        with col2:
            cancel = st.form_submit_button("❌ Annuler")

        if submitted:
            if validate_info_form(prenom, nom, email):
                success = update_consultant_info(
                    consultant.id,
                    {
                        "prenom": prenom,
                        "nom": nom,
                        "email": email,
                        "telephone": telephone,
                        "salaire_actuel": salaire_actuel,
                        "disponibilite": disponibilite,
                        "notes": notes,
                        "commentaire": motif_changement,
                    },
                )

                if success:
                    st.success("✅ Informations mises à jour !")
                    del st.session_state.edit_consultant_info
                    st.rerun()
                else:
                    st.error(MSG_ERREUR_MISE_A_JOUR)
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
            existing = (
                session.query(Consultant)
                .filter(Consultant.email == data["email"], Consultant.id != consultant_id)
                .first()
            )
            if existing:
                st.error("❌ Cet email est déjà utilisé par un autre consultant")
                return False

            # Sauvegarder l'ancien salaire si changé
            old_salary = consultant.salaire_actuel
            new_salary = data["salaire_actuel"]

            if old_salary != new_salary and data.get("commentaire"):
                salary_history = ConsultantSalaire(
                    consultant_id=consultant_id,
                    salaire=old_salary,
                    date_debut=datetime.now(),
                    commentaire=data["commentaire"],
                )
                session.add(salary_history)

            # Mettre à jour les informations
            consultant.prenom = data["prenom"].strip()
            consultant.nom = data["nom"].strip()
            consultant.email = data["email"].strip().lower()
            consultant.telephone = data["telephone"].strip() if data["telephone"] else None
            consultant.salaire_actuel = new_salary
            consultant.disponibilite = data["disponibilite"]
            consultant.notes = data["notes"].strip() if data["notes"] else None

            session.commit()

            st.info("✅ Informations du consultant mises à jour")
            return True

    except Exception as e:
        st.error(f"{MSG_ERREUR_MISE_A_JOUR}: {e}")
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
                competence_count = (
                    session.query(ConsultantCompetence)
                    .filter(ConsultantCompetence.consultant_id == consultant.id)
                    .count()
                )

                mission_count = session.query(Mission).filter(Mission.consultant_id == consultant.id).count()

            st.write(f"**Nombre de compétences :** {competence_count}")
            st.write(f"**Nombre de missions :** {mission_count}")

        except Exception as e:
            st.warning(f"⚠️ Impossible de charger les statistiques: {e}")

        st.success("✅ Rapport généré avec succès !")

    except Exception as e:
        st.error(f"{MSG_ERREUR_RAPPORT}: {e}")
