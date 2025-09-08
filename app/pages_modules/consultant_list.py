"""
Module de gestion de la liste des consultants
Fonctions pour afficher, filtrer et rechercher les consultants
"""

import os
import sys
from datetime import datetime
from typing import List
from typing import Optional

import pandas as pd
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
    from sqlalchemy.orm import joinedload

    from database.database import get_database_session
    from database.models import Competence
    from database.models import Consultant
    from database.models import ConsultantCompetence
    from database.models import ConsultantSalaire
    from database.models import Mission
    from services.consultant_service import ConsultantService

    imports_ok = True
except ImportError as e:
    # Imports échoués, on continue quand même
    pass


def show_consultants_list():
    """Affiche la liste des consultants avec filtres et recherche"""

    if not imports_ok:
        st.error("❌ Les services de base ne sont pas disponibles")
        return

    st.markdown("### 📋 Liste des consultants")

    # Récupérer tous les consultants
    try:
        with get_database_session() as session:
            consultants = (
                session.query(Consultant).options(joinedload(Consultant.practice)).all()
            )

        if not consultants:
            st.info("ℹ️ Aucun consultant trouvé dans la base de données")
            return

        # Convertir en DataFrame pour faciliter la manipulation
        consultants_data = []
        for consultant in consultants:
            practice_name = (
                consultant.practice.nom if consultant.practice else "Non affecté"
            )

            consultants_data.append(
                {
                    "ID": consultant.id,
                    "Prénom": consultant.prenom,
                    "Nom": consultant.nom,
                    "Email": consultant.email,
                    "Téléphone": consultant.telephone,
                    "Salaire annuel": consultant.salaire_actuel or 0,
                    "Disponibilité": (
                        "✅ Disponible" if consultant.disponibilite else "🔴 En mission"
                    ),
                    "Date disponibilité": consultant.date_disponibilite,  # Nouveau champ V1.2.2
                    "Grade": consultant.grade,
                    "Type contrat": consultant.type_contrat,
                    "Practice": practice_name,
                    "Date création": (
                        consultant.date_creation.strftime("%d/%m/%Y")
                        if consultant.date_creation
                        else "N/A"
                    ),
                }
            )

        df = pd.DataFrame(consultants_data)

        # Filtres et recherche
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            search_term = st.text_input(
                "🔍 Recherche",
                placeholder="Nom, prénom, email...",
                help="Rechercher par nom, prénom ou email",
            )

        with col2:
            practice_filter = st.selectbox(
                "🏢 Filtrer par practice",
                options=["Tous"] + sorted(list(set(df["Practice"].tolist()))),
                help="Filtrer les consultants par practice",
            )

        with col3:
            availability_filter = st.selectbox(
                "📊 Statut",
                options=["Tous", "Disponible", "En mission"],
                help="Filtrer par disponibilité",
            )

        # Appliquer les filtres
        filtered_df = df.copy()

        if search_term:
            filtered_df = filtered_df[
                filtered_df["Prénom"].str.contains(search_term, case=False, na=False)
                | filtered_df["Nom"].str.contains(search_term, case=False, na=False)
                | filtered_df["Email"].str.contains(search_term, case=False, na=False)
            ]

        if practice_filter != "Tous":
            filtered_df = filtered_df[filtered_df["Practice"] == practice_filter]

        if availability_filter != "Tous":
            status_map = {"Disponible": "✅ Disponible", "En mission": "🔴 En mission"}
            filtered_df = filtered_df[
                filtered_df["Disponibilité"] == status_map[availability_filter]
            ]

        # Statistiques
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_consultants = len(filtered_df)
            st.metric("👥 Total consultants", total_consultants)

        with col2:
            available_count = len(
                filtered_df[filtered_df["Disponibilité"] == "✅ Disponible"]
            )
            st.metric("✅ Disponibles", available_count)

        with col3:
            busy_count = len(
                filtered_df[filtered_df["Disponibilité"] == "🔴 En mission"]
            )
            st.metric("🔴 En mission", busy_count)

        with col4:
            total_salary = filtered_df["Salaire annuel"].sum()
            st.metric("💰 Masse salariale", f"{total_salary:,.0f}€")

        st.markdown("---")

        # Affichage du tableau
        if filtered_df.empty:
            st.info("ℹ️ Aucun consultant ne correspond aux critères de recherche")
        else:
            # Configuration des colonnes à afficher
            display_columns = [
                "Prénom",
                "Nom",
                "Email",
                "Disponibilité",
                "Date disponibilité",
                "Grade",
                "Type contrat",
                "Practice",
            ]

            # Afficher le DataFrame avec sélection interactive (comme dans business
            # managers)
            event = st.dataframe(
                filtered_df[display_columns],
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row",
                column_config={
                    "Prénom": st.column_config.TextColumn("Prénom", width="small"),
                    "Nom": st.column_config.TextColumn("Nom", width="small"),
                    "Email": st.column_config.TextColumn("Email", width="large"),
                    "Disponibilité": st.column_config.TextColumn(
                        "Disponibilité", width="small"
                    ),
                    "Date disponibilité": st.column_config.TextColumn(
                        "Date disponibilité", width="small"
                    ),
                    "Grade": st.column_config.TextColumn("Grade", width="small"),
                    "Type contrat": st.column_config.TextColumn(
                        "Type contrat", width="small"
                    ),
                    "Practice": st.column_config.TextColumn("Practice", width="medium"),
                },
            )

            # Actions sur sélection (comme dans business managers)
            if event.selection.rows:
                selected_row = event.selection.rows[0]
                # Récupérer les données depuis le DataFrame filtré
                selected_consultant_data = filtered_df.iloc[selected_row]
                # S'assurer que c'est un int
                selected_id = int(selected_consultant_data["ID"])
                selected_name = f"{
                    selected_consultant_data['Prénom']} {
                    selected_consultant_data['Nom']}"

                st.success(
                    f"✅ Consultant sélectionné : **{selected_name}** (ID: {selected_id})"
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button(
                        "👁️ Voir le profil",
                        type="primary",
                        use_container_width=True,
                        key=f"view_profile_{selected_id}",
                    ):
                        st.session_state.view_consultant_profile = selected_id
                        st.rerun()

                with col2:
                    if st.button(
                        "✏️ Modifier",
                        use_container_width=True,
                        key=f"edit_profile_{selected_id}",
                    ):
                        # Pour l'instant, on redirige vers le profil avec mode édition
                        st.session_state.view_consultant_profile = selected_id
                        st.session_state.edit_consultant_mode = True
                        st.rerun()

                with col3:
                    if st.button(
                        "🗑️ Supprimer",
                        use_container_width=True,
                        key=f"delete_profile_{selected_id}",
                    ):
                        # Pour l'instant, on redirige vers le profil avec mode
                        # suppression
                        st.session_state.view_consultant_profile = selected_id
                        st.session_state.delete_consultant_mode = True
                        st.rerun()

            # Sélection alternative avec selectbox (gardé pour compatibilité)
            st.markdown("---")
            st.markdown("### 🔍 Sélection alternative")

            # Sélection d'un consultant pour voir le détail
            selected_consultant = st.selectbox(
                "👤 Ou sélectionner un consultant pour voir son profil détaillé",
                options=[""]
                + [
                    f"{row['Prénom']} {row['Nom']} (ID: {row['ID']})"
                    for _, row in filtered_df.iterrows()
                ],
                help="Choisissez un consultant pour accéder à son profil complet",
            )

            if selected_consultant:
                # Extraire l'ID du consultant sélectionné
                import re

                match = re.search(r"\(ID: (\d+)\)", selected_consultant)
                if match:
                    consultant_id = int(match.group(1))

                    if st.button(
                        "👁️ Voir le profil détaillé",
                        key=f"view_profile_alt_{consultant_id}",
                    ):
                        st.session_state.view_consultant_profile = consultant_id
                        st.rerun()

            # Boutons d'actions groupées
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button(
                    "📊 Exporter en Excel", help="Télécharger la liste au format Excel"
                ):
                    export_to_excel(filtered_df)

            with col2:
                if st.button("📈 Générer rapport", help="Créer un rapport détaillé"):
                    generate_consultants_report(filtered_df)

            with col3:
                if st.button("🔄 Actualiser", help="Recharger les données"):
                    st.rerun()

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement de la liste des consultants: {e}")
        st.code(str(e))


def export_to_excel(df: pd.DataFrame):
    """Exporte les données des consultants vers Excel"""

    try:
        # Créer un buffer pour le fichier Excel
        from io import BytesIO

        import openpyxl
        from openpyxl.styles import Font
        from openpyxl.styles import PatternFill

        # Créer le workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Consultants"

        # En-têtes avec style
        headers = list(df.columns)
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num, value=header)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(
                start_color="1f77b4", end_color="1f77b4", fill_type="solid"
            )

        # Données
        for row_num, row in enumerate(df.itertuples(index=False), 2):
            for col_num, value in enumerate(row, 1):
                ws.cell(row=row_num, column=col_num, value=value)

        # Ajuster la largeur des colonnes
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except BaseException:
                    pass
            adjusted_width = min(max_length + 2, 50)  # Largeur max de 50
            ws.column_dimensions[column_letter].width = adjusted_width

        # Sauvegarder dans un buffer
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        # Bouton de téléchargement
        st.download_button(
            label="📥 Télécharger Excel",
            data=buffer,
            file_name=f"consultants_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        st.success("✅ Fichier Excel généré avec succès !")

    except ImportError:
        st.error(
            "❌ Module openpyxl non installé. Installez-le avec : pip install openpyxl"
        )
    except Exception as e:
        st.error(f"❌ Erreur lors de l'export Excel: {e}")


def generate_consultants_report(df: pd.DataFrame):
    """Génère un rapport détaillé des consultants"""

    try:
        st.markdown("### 📊 Rapport des consultants")

        # Statistiques générales
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("👥 Effectif")
            st.metric("Total", len(df))
            available = len(df[df["Disponibilité"] == "✅ Disponible"])
            st.metric("Disponibles", f"{available} ({available / len(df) * 100:.1f}%)")

        with col2:
            st.subheader("💰 Rémunération")
            total_salary = df["Salaire annuel"].sum()
            avg_salary = df["Salaire annuel"].mean()
            st.metric("Masse salariale", f"{total_salary:,.0f}€")
            st.metric("Salaire moyen", f"{avg_salary:,.0f}€")

        with col3:
            st.subheader("🏢 Répartition")
            practice_counts = df["Practice"].value_counts()
            for practice, count in practice_counts.items():
                st.metric(practice, count)

        # Graphiques
        st.markdown("### 📈 Visualisations")

        # Répartition par practice
        if len(practice_counts) > 1:
            st.bar_chart(practice_counts)

        # Distribution des salaires
        if len(df) > 1:
            salary_data = df[["Prénom", "Nom", "Salaire annuel"]].copy()
            salary_data["Nom complet"] = (
                salary_data["Prénom"] + " " + salary_data["Nom"]
            )
            salary_data = salary_data.sort_values("Salaire annuel", ascending=False)

            st.bar_chart(
                salary_data.set_index("Nom complet")["Salaire annuel"],
                use_container_width=True,
            )

        st.success("✅ Rapport généré avec succès !")

    except Exception as e:
        st.error(f"❌ Erreur lors de la génération du rapport: {e}")
