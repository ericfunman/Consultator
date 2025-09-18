"""
Page de gestion des practices - VERSION FONCTIONNELLE
"""

import streamlit as st
from services.practice_service import PracticeService


def show():
    """Affiche la page de gestion des practices"""
    st.title("🏢 Gestion des Practices")

    # Onglets pour organiser les fonctionnalités
    tab1, tab2, tab3 = st.tabs(
        ["📊 Vue d'ensemble", "👥 Consultants par Practice", "⚙️ Gestion des Practices"]
    )

    with tab1:
        show_practice_overview()

    with tab2:
        show_consultants_by_practice()

    with tab3:
        show_practice_management()


def show_practice_overview():
    """Affiche une vue d'ensemble des practices"""
    st.subheader("📊 Vue d'ensemble des Practices")

    try:
        # Récupérer les statistiques
        stats = PracticeService.get_practice_statistics()

        if stats:
            # Afficher les métriques principales
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Practices", stats.get("total_practices", 0))

            with col2:
                st.metric("Consultants assignés", stats.get("total_consultants", 0))

            with col3:
                st.metric("Practices actives", stats.get("active_practices", 0))

        # Afficher la liste des practices
        practices = PracticeService.get_all_practices()
        if practices:
            st.subheader("Liste des Practices")
            for practice in practices:
                with st.expander(f"🏢 {practice.nom}"):
                    st.write(
                        f"**Description:** {practice.description or 'Aucune description'}"
                    )
                    st.write(f"**Responsable:** {practice.responsable or 'Non défini'}")
                    st.write(
                        f"**Statut:** {'✅ Actif' if practice.actif else '❌ Inactif'}"
                    )

    except Exception as e:
        st.error(f"Erreur lors du chargement de la vue d'ensemble: {e}")


def show_consultants_by_practice():
    """Affiche les consultants par practice"""
    st.subheader("👥 Consultants par Practice")

    try:
        practices = PracticeService.get_all_practices()

        if practices:
            selected_practice = st.selectbox(
                "Sélectionner une practice:",
                options=practices,
                format_func=lambda x: x.nom,
            )

            if selected_practice:
                consultants = PracticeService.get_consultants_by_practice(
                    selected_practice.id
                )

                if consultants:
                    st.write(
                        f"**{len(consultants)} consultant(s) dans la practice {selected_practice.nom}:**"
                    )
                    for consultant in consultants:
                        st.write(f"• {consultant.prenom} {consultant.nom}")
                else:
                    st.info("Aucun consultant assigné à cette practice.")
        else:
            st.warning("Aucune practice trouvée.")

    except Exception as e:
        st.error(f"Erreur lors du chargement des consultants: {e}")


def show_practice_management():
    """Interface de gestion des practices"""
    st.subheader("⚙️ Gestion des Practices")

    # Créer une nouvelle practice
    with st.expander("➕ Créer une nouvelle practice"):
        with st.form("create_practice_form"):
            nom = st.text_input("Nom de la practice*")
            description = st.text_area("Description")
            responsable = st.text_input("Responsable")

            if st.form_submit_button("Créer la practice"):
                if nom:
                    try:
                        success = PracticeService.create_practice(
                            nom=nom, description=description, responsable=responsable
                        )
                        if success:
                            st.success(f"✅ Practice '{nom}' créée avec succès !")
                            st.rerun()
                        else:
                            st.error("❌ Erreur lors de la création de la practice.")
                    except Exception as e:
                        st.error(f"❌ Erreur: {e}")
                else:
                    st.error("❌ Le nom de la practice est obligatoire.")

    # Modifier/supprimer des practices existantes
    practices = PracticeService.get_all_practices()
    if practices:
        st.write("**Practices existantes:**")
        for practice in practices:
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.write(f"🏢 {practice.nom}")

            with col2:
                if st.button(f"Modifier", key=f"edit_{practice.id}"):
                    st.info("Fonction de modification en cours de développement")

            with col3:
                status = "✅ Actif" if practice.actif else "❌ Inactif"
                st.write(status)
