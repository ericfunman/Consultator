"""
Page de gestion des practices - VERSION OPTIMISÉE
Performance améliorée avec cache, pagination et requêtes SQL optimisées
"""

import time
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from services.consultant_service import ConsultantService
from services.practice_service_optimized import PracticeServiceOptimized


def show():
    """Affiche la page de gestion des practices optimisée"""

    st.title("🏢 Gestion des Practices")

    # Mesurer le temps de chargement
    start_time = time.time()

    # Onglets pour organiser les fonctionnalités
    tab1, tab2, tab3 = st.tabs(
        ["📊 Vue d'ensemble", "👥 Consultants par Practice", "⚙️ Gestion des Practices"])

    with tab1:
        show_practice_overview_optimized()

    with tab2:
        show_consultants_by_practice_optimized()

    with tab3:
        show_practice_management_optimized()

    # Afficher le temps de chargement en bas de page
    end_time = time.time()
    loading_time = end_time - start_time
    st.caption(f"⚡ Temps de chargement: {loading_time:.2f}s")


def show_practice_overview_optimized():
    """Affiche une vue d'ensemble des practices - VERSION OPTIMISÉE"""

    # Récupérer les statistiques avec cache
    with st.spinner("🔄 Chargement des statistiques..."):
        stats = PracticeServiceOptimized.get_practice_statistics_optimized()

    # Métriques principales
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="🏢 Total Practices",
            value=stats["total_practices"]
        )

    with col2:
        st.metric(
            label="👥 Total Consultants",
            value=stats["total_consultants"]
        )

    with col3:
        consultants_actifs = sum([p["consultants_actifs"]
                                 for p in stats["practices_detail"]])
        taux_activite = (
            consultants_actifs /
            stats["total_consultants"] *
            100) if stats["total_consultants"] > 0 else 0
        st.metric(
            label="✅ Consultants Actifs",
            value=consultants_actifs,
            delta=f"{taux_activite:.1f}% du total"
        )

    st.markdown("---")

    # Tableau détaillé par practice
    if stats["practices_detail"]:
        st.subheader("📋 Détail par Practice")

        df_practices = pd.DataFrame(stats["practices_detail"])
        df_practices = df_practices.rename(columns={
            "nom": "Practice",
            "total_consultants": "Total Consultants",
            "consultants_actifs": "Consultants Actifs",
            "responsable": "Responsable"
        })

        # Calculer le taux d'activité
        df_practices["Taux Activité"] = (
            df_practices["Consultants Actifs"] / df_practices["Total Consultants"] * 100
        ).round(1).astype(str) + "%"

        # Afficher le tableau avec formatting
        st.dataframe(
            df_practices, use_container_width=True, hide_index=True, column_config={
                "Practice": st.column_config.TextColumn(
                    "Practice", width="medium"), "Total Consultants": st.column_config.NumberColumn(
                    "Total", width="small"), "Consultants Actifs": st.column_config.NumberColumn(
                    "Actifs", width="small"), "Taux Activité": st.column_config.TextColumn(
                        "Taux", width="small"), "Responsable": st.column_config.TextColumn(
                            "Responsable", width="medium")})

        # Graphiques optimisés
        if len(df_practices) > 0:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📈 Répartition des Consultants")
                chart_data = df_practices.set_index(
                    "Practice")[["Total Consultants", "Consultants Actifs"]]
                st.bar_chart(chart_data, height=300)

            with col2:
                st.subheader("🎯 Taux d'activité par Practice")
                # Graphique en secteurs avec Plotly
                if len(df_practices) > 0:
                    # Préparer les données pour le graphique en secteurs
                    fig = px.pie(
                        df_practices,
                        values='Consultants Actifs',
                        names='Practice',
                        title="Répartition des consultants actifs",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    fig.update_layout(height=300, showlegend=True)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Pas assez de données pour le graphique")

    else:
        st.info(
            "ℹ️ Aucune practice trouvée. Créez votre première practice dans l'onglet 'Gestion des Practices'.")


def show_consultants_by_practice_optimized():
    """Affiche les consultants regroupés par practice - VERSION OPTIMISÉE avec pagination"""

    # Configuration pagination
    if 'practice_page' not in st.session_state:
        st.session_state.practice_page = 1

    per_page = 25  # Nombre de consultants par page

    # Récupérer les practices pour le filtre
    practices_cached = PracticeServiceOptimized.get_all_practices_cached()
    practices_names = [p['nom'] for p in practices_cached]

    # Filtre par practice
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        selected_practice = st.selectbox(
            "🔍 Filtrer par Practice",
            options=["Toutes"] + practices_names + ["Sans Practice"],
            index=0,
            key="practice_filter"
        )

    with col2:
        if st.button("🔄 Actualiser", key="refresh_consultants"):
            PracticeServiceOptimized.clear_practices_cache()
            st.rerun()

    with col3:
        per_page = st.selectbox("Consultants par page", [10, 25, 50, 100], index=1)

    st.markdown("---")

    # Récupération paginée des consultants
    with st.spinner("🔄 Chargement des consultants..."):
        consultants, total = PracticeServiceOptimized.get_consultants_by_practice_paginated(
            practice_name=selected_practice if selected_practice != "Toutes" else None,
            page=st.session_state.practice_page,
            per_page=per_page
        )

    if consultants:
        # Affichage des informations de pagination
        total_pages = (total + per_page - 1) // per_page
        st.info(
            f"📊 {total} consultant(s) trouvé(s) - Page {st.session_state.practice_page}/{total_pages}")

        # Afficher les consultants par practice
        current_practice = None
        practice_consultants = []

        for consultant in consultants:
            if consultant["practice_nom"] != current_practice:
                # Afficher la practice précédente si elle existe
                if practice_consultants:
                    show_practice_consultants_optimized(
                        current_practice, practice_consultants)

                # Nouvelle practice
                current_practice = consultant["practice_nom"]
                practice_consultants = []

            practice_consultants.append(consultant)

        # Afficher la dernière practice
        if practice_consultants:
            show_practice_consultants_optimized(current_practice, practice_consultants)

        # Navigation pagination
        if total_pages > 1:
            st.markdown("---")
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                if st.button(
                    "⏮️ Première", disabled=(
                        st.session_state.practice_page == 1)):
                    st.session_state.practice_page = 1
                    st.rerun()

            with col2:
                if st.button(
                    "⬅️ Précédente", disabled=(
                        st.session_state.practice_page == 1)):
                    st.session_state.practice_page -= 1
                    st.rerun()

            with col3:
                # Sélecteur de page direct
                new_page = st.selectbox(
                    "Page",
                    range(1, total_pages + 1),
                    index=st.session_state.practice_page - 1,
                    key="page_selector"
                )
                if new_page != st.session_state.practice_page:
                    st.session_state.practice_page = new_page
                    st.rerun()

            with col4:
                if st.button(
                    "➡️ Suivante", disabled=(
                        st.session_state.practice_page == total_pages)):
                    st.session_state.practice_page += 1
                    st.rerun()

            with col5:
                if st.button(
                    "⏭️ Dernière", disabled=(
                        st.session_state.practice_page == total_pages)):
                    st.session_state.practice_page = total_pages
                    st.rerun()

    else:
        st.info("ℹ️ Aucun consultant trouvé pour cette practice.")


def show_practice_consultants_optimized(practice_name: str, consultants: list):
    """Affiche les consultants d'une practice - VERSION OPTIMISÉE"""

    if not consultants:
        st.markdown(f"### 🏢 {practice_name}")
        st.info("Aucun consultant dans cette practice")
        return

    st.markdown(
        f"### 🏢 {practice_name} ({
            len(consultants)} consultant{
            's' if len(consultants) > 1 else ''})")

    # Créer un DataFrame optimisé (données déjà préparées)
    consultants_data = []
    for consultant in consultants:
        # Gérer les deux formats possibles
        nom_complet = consultant.get("nom_complet") or f"{
            consultant.get(
                'prenom', '')} {
            consultant.get(
                'nom', '')}".strip()

        consultants_data.append(
            {
                "Nom": nom_complet,
                "Email": consultant.get("email") or "Non renseigné",
                "Téléphone": consultant.get("telephone") or "Non renseigné",
                "Salaire": f"{
                    consultant.get(
                        'salaire_actuel',
                        0):,.0f} €" if consultant.get("salaire_actuel") else "Non renseigné",
                "Disponible": "✅" if consultant.get("disponibilite") else "❌",
                "Missions": consultant.get(
                    "nb_missions",
                    0),
                "Compétences": consultant.get(
                    "nb_competences",
                    0)})

    if consultants_data:
        df = pd.DataFrame(consultants_data)

        # Afficher le tableau optimisé
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Nom": st.column_config.TextColumn("Nom", width="medium"),
                "Email": st.column_config.TextColumn("Email", width="medium"),
                "Téléphone": st.column_config.TextColumn("Téléphone", width="small"),
                "Salaire": st.column_config.TextColumn("Salaire", width="small"),
                "Disponible": st.column_config.TextColumn("Dispo", width="small"),
                "Missions": st.column_config.NumberColumn("Missions", width="small"),
                "Compétences": st.column_config.NumberColumn("Compétences", width="small")
            }
        )

        # Actions rapides
        with st.expander(f"⚡ Actions rapides - {practice_name}"):
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button(
                        f"📊 Statistiques détaillées",
                        key=f"stats_{practice_name}"):
                    show_practice_detailed_stats_cached(practice_name)

            with col2:
                if st.button(f"📧 Exporter emails", key=f"export_{practice_name}"):
                    emails = [c["email"] for c in consultants if c["email"]
                              and c["email"] != "Non renseigné"]
                    if emails:
                        st.code("; ".join(emails))
                        st.success(f"✅ {len(emails)} emails copiés")
                    else:
                        st.warning("Aucun email valide trouvé")

            with col3:
                # Statistiques rapides
                disponibles = len([c for c in consultants if c["disponibilite"]])
                st.metric("Disponibles", disponibles, f"sur {len(consultants)}")

    st.markdown("---")


def show_practice_detailed_stats_cached(practice_name: str):
    """Affiche des statistiques détaillées pour une practice avec cache"""

    st.subheader(f"📊 Statistiques détaillées - {practice_name}")

    # Utiliser le cache pour les stats détaillées
    with st.spinner("Calcul des statistiques..."):
        stats = PracticeServiceOptimized.get_practice_detailed_stats_cached(
            practice_name)

    if stats:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("👥 Total Consultants", stats["total_consultants"])

        with col2:
            st.metric("✅ Disponibles", stats["disponibles"])

        with col3:
            if stats["salaire_moyen"] > 0:
                st.metric("💰 Salaire Moyen", f"{stats['salaire_moyen']:,.0f} €")
            else:
                st.metric("💰 Salaire Moyen", "N/A")

        with col4:
            st.metric("🎯 Total Missions", stats["total_missions"])

        # Métriques supplémentaires
        col5, col6 = st.columns(2)

        with col5:
            st.metric("🔧 Total Compétences", stats["total_competences"])

        with col6:
            if stats["total_consultants"] > 0:
                taux_dispo = (stats["disponibles"] / stats["total_consultants"]) * 100
                st.metric("📈 Taux Disponibilité", f"{taux_dispo:.1f}%")
    else:
        st.info("Aucune donnée disponible")


def show_practice_management_optimized():
    """Interface de gestion des practices optimisée"""

    st.subheader("⚙️ Gestion des Practices")

    # Récupérer les practices avec cache
    practices_cached = PracticeServiceOptimized.get_all_practices_cached()

    # Onglets pour les différentes actions
    mgmt_tab1, mgmt_tab2, mgmt_tab3 = st.tabs(
        ["➕ Créer Practice", "✏️ Modifier Practice", "👤 Assigner Consultants"])

    with mgmt_tab1:
        show_create_practice_form_optimized()

    with mgmt_tab2:
        show_edit_practice_form_optimized(practices_cached)

    with mgmt_tab3:
        show_assign_consultant_form_optimized(practices_cached)


def show_create_practice_form_optimized():
    """Formulaire de création de practice optimisé"""

    st.markdown("#### ➕ Créer une nouvelle Practice")

    with st.form("create_practice_form"):
        col1, col2 = st.columns(2)

        with col1:
            nom = st.text_input(
                "Nom de la Practice *",
                placeholder="Ex: DevOps, Cloud, etc."
            )

        with col2:
            responsable = st.text_input(
                "Responsable",
                placeholder="Nom du responsable (optionnel)"
            )

        description = st.text_area(
            "Description",
            placeholder="Description de la practice (optionnel)"
        )

        submitted = st.form_submit_button("🚀 Créer la Practice", type="primary")

        if submitted:
            if not nom.strip():
                st.error("❌ Le nom de la practice est obligatoire")
            else:
                # Utiliser le service original pour la création
                from services.practice_service import PracticeService
                practice = PracticeService.create_practice(
                    nom=nom.strip(),
                    description=description.strip(),
                    responsable=responsable.strip()
                )

                if practice:
                    # Effacer le cache après création
                    PracticeServiceOptimized.clear_practices_cache()
                    st.rerun()


def show_edit_practice_form_optimized(practices_cached: list):
    """Formulaire de modification de practice optimisé"""

    st.markdown("#### ✏️ Modifier une Practice")

    if not practices_cached:
        st.info("Aucune practice à modifier")
        return

    # Sélection de la practice à modifier
    practice_options = {f"{p['nom']}": p for p in practices_cached}
    selected_name = st.selectbox(
        "Sélectionner la practice à modifier",
        options=list(practice_options.keys())
    )

    if selected_name:
        practice = practice_options[selected_name]

        with st.form(f"edit_practice_form_{practice['id']}"):
            col1, col2 = st.columns(2)

            with col1:
                new_nom = st.text_input(
                    "Nom de la Practice *",
                    value=practice['nom']
                )

            with col2:
                new_responsable = st.text_input(
                    "Responsable",
                    value=practice['responsable'] or ""
                )

            new_description = st.text_area(
                "Description",
                value=practice['description'] or ""
            )

            new_actif = st.checkbox(
                "Practice active",
                value=practice['actif']
            )

            submitted = st.form_submit_button(
                "💾 Sauvegarder les modifications", type="primary")

            if submitted:
                if not new_nom.strip():
                    st.error("❌ Le nom de la practice est obligatoire")
                else:
                    # Utiliser le service original pour la modification
                    from services.practice_service import PracticeService
                    success = PracticeService.update_practice(
                        practice['id'],
                        nom=new_nom.strip(),
                        description=new_description.strip(),
                        responsable=new_responsable.strip(),
                        actif=new_actif
                    )

                    if success:
                        # Effacer le cache après modification
                        PracticeServiceOptimized.clear_practices_cache()
                        st.rerun()


def show_assign_consultant_form_optimized(practices_cached: list):
    """Formulaire d'assignation de consultants aux practices optimisé"""

    st.markdown("#### 👤 Assigner des Consultants aux Practices")

    # Récupérer tous les consultants (utiliser cache si possible)
    consultants = ConsultantService.get_all_consultants()

    if not consultants:
        st.info("Aucun consultant trouvé")
        return

    # Sélection du consultant
    consultant_options = {}
    for c in consultants:
        if hasattr(c, 'nom_complet') and hasattr(c, 'email'):
            # Objet Consultant avec propriétés
            consultant_options[f"{c.nom_complet} ({c.email})"] = c
        elif isinstance(c, dict):
            # Dict avec nom et prenom séparés
            nom_complet = f"{c.get('prenom', '')} {c.get('nom', '')}".strip()
            email = c.get('email', 'Pas d\'email')
            consultant_options[f"{nom_complet} ({email})"] = c
        else:
            # Gestion défensive pour autres formats
            nom_complet = getattr(
                c, 'nom_complet', f"{
                    getattr(
                        c, 'prenom', '')} {
                    getattr(
                        c, 'nom', '')}".strip())
            email = getattr(c, 'email', 'Pas d\'email')
            consultant_options[f"{nom_complet} ({email})"] = c
    selected_consultant_name = st.selectbox(
        "Sélectionner le consultant",
        options=list(consultant_options.keys())
    )

    if selected_consultant_name:
        consultant = consultant_options[selected_consultant_name]

        # Afficher la practice actuelle
        try:
            if hasattr(consultant, 'practice') and consultant.practice:
                current_practice = consultant.practice.nom
            elif isinstance(consultant, dict) and consultant.get('practice'):
                current_practice = consultant.get('practice', {}).get('nom', 'Aucune')
            else:
                current_practice = "Aucune"
        except BaseException:
            current_practice = "Aucune"
        st.info(f"Practice actuelle : **{current_practice}**")

        # Sélection de la nouvelle practice
        practice_options = {"Aucune practice": None}
        practice_options.update({p['nom']: p['id'] for p in practices_cached})

        selected_practice = st.selectbox(
            "Nouvelle practice",
            options=list(practice_options.keys()),
            index=0
        )

        if st.button("🔄 Assigner à la practice", type="primary"):
            practice_id = practice_options[selected_practice]

            # Utiliser le service original pour l'assignation
            from services.practice_service import PracticeService

            # Récupérer l'ID du consultant de manière défensive
            consultant_id = None
            if hasattr(consultant, 'id'):
                consultant_id = consultant.id
            elif isinstance(consultant, dict):
                consultant_id = consultant.get('id')

            if consultant_id:
                success = PracticeService.assign_consultant_to_practice(
                    consultant_id,
                    practice_id
                )

                if success:
                    # Effacer le cache après assignation
                    PracticeServiceOptimized.clear_practices_cache()
                    st.success("✅ Consultant assigné avec succès !")
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de l'assignation")
            else:
                st.error("❌ Impossible de récupérer l'ID du consultant")
