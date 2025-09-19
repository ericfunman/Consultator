"""
Page de gestion des practices - VERSION FONCTIONNELLE
"""

import streamlit as st
try:
    import pandas as pd
except ImportError:
    pd = None

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
    """Affiche les consultants par practice avec gestion avancée"""
    st.subheader("👥 Consultants par Practice")

    try:
        practices = PracticeService.get_all_practices()

        if practices:
            # Colonnes pour l'interface
            col1, col2 = st.columns([2, 1])
            
            with col1:
                selected_practice = st.selectbox(
                    "Sélectionner une practice:",
                    options=practices,
                    format_func=lambda x: x.nom,
                    key="practice_selector"
                )

            if selected_practice:
                # Onglets pour organiser les actions
                tab1, tab2, tab3 = st.tabs(["📋 Liste des consultants", "➕ Affecter consultant", "⚙️ Actions"])
                
                with tab1:
                    # Récupérer les consultants de la practice
                    consultants_dict = PracticeService.get_consultants_by_practice(
                        selected_practice.id
                    )

                    if consultants_dict:
                        practice_name = list(consultants_dict.keys())[0]
                        consultants = consultants_dict[practice_name]
                        
                        if consultants:
                            st.write(f"**{len(consultants)} consultant(s) dans la practice {selected_practice.nom}**")
                            
                            # Tableau interactif des consultants
                            consultant_data = []
                            for consultant in consultants:
                                consultant_data.append({
                                    "ID": consultant.id,
                                    "Nom": consultant.nom,
                                    "Prénom": consultant.prenom,
                                    "Email": consultant.email,
                                    "Grade": getattr(consultant, 'grade', 'Non défini'),
                                    "Disponible": "✅" if getattr(consultant, 'disponibilite', False) else "❌",
                                    "Salaire": f"{getattr(consultant, 'salaire_actuel', 0):,.0f}€" if getattr(consultant, 'salaire_actuel', None) else "Non défini"
                                })
                            
                            if consultant_data:
                                if pd is not None:
                                    df = pd.DataFrame(consultant_data)
                                    
                                    # Affichage du tableau avec possibilité de sélection
                                    st.dataframe(
                                        df, 
                                        use_container_width=True,
                                        hide_index=True,
                                        column_config={
                                            "ID": st.column_config.NumberColumn("ID", width="small"),
                                            "Nom": st.column_config.TextColumn("Nom", width="medium"),
                                            "Prénom": st.column_config.TextColumn("Prénom", width="medium"),
                                            "Email": st.column_config.TextColumn("Email", width="large"),
                                            "Grade": st.column_config.TextColumn("Grade", width="medium"),
                                            "Disponible": st.column_config.TextColumn("Disponible", width="small"),
                                            "Salaire": st.column_config.TextColumn("Salaire", width="medium")
                                        }
                                    )
                                else:
                                    # Affichage simple sans pandas
                                    for data in consultant_data:
                                        st.write(f"**{data['Prénom']} {data['Nom']}** - {data['Grade']} - {data['Email']} - {data['Salaire']}")
                                
                                # Section pour retirer un consultant
                                st.write("**Retirer un consultant de la practice:**")
                                consultant_to_remove = st.selectbox(
                                    "Choisir un consultant à retirer:",
                                    options=consultants,
                                    format_func=lambda x: f"{x.prenom} {x.nom}",
                                    key="consultant_to_remove"
                                )
                                
                                if st.button("🗑️ Retirer de la practice", key="remove_consultant"):
                                    try:
                                        # Retirer l'affectation (mettre practice_id à None)
                                        success = PracticeService.assign_consultant_to_practice(
                                            consultant_to_remove.id, None
                                        )
                                        if success:
                                            st.success(f"✅ {consultant_to_remove.prenom} {consultant_to_remove.nom} a été retiré de la practice {selected_practice.nom}")
                                            st.rerun()
                                        else:
                                            st.error("❌ Erreur lors du retrait du consultant")
                                    except Exception as e:
                                        st.error(f"❌ Erreur: {e}")
                        else:
                            st.info("Aucun consultant assigné à cette practice.")
                    else:
                        st.info("Aucun consultant assigné à cette practice.")
                
                with tab2:
                    # Section pour affecter un nouveau consultant
                    st.write("**Affecter un consultant à la practice:**")
                    
                    # Récupérer les consultants sans practice ou d'autres practices
                    from app.services.consultant_service import ConsultantService
                    all_consultants = ConsultantService.get_all_consultants_objects(page=1, per_page=10000)  # Récupérer tous les consultants
                    
                    # Filtrer les consultants pas encore dans cette practice
                    available_consultants = [
                        c for c in all_consultants 
                        if not c.practice_id or c.practice_id != selected_practice.id
                    ]
                    
                    if available_consultants:
                        consultant_to_add = st.selectbox(
                            "Choisir un consultant à affecter:",
                            options=available_consultants,
                            format_func=lambda x: f"{x.prenom} {x.nom} - {getattr(x, 'grade', 'Grade non défini')}",
                            key="consultant_to_add"
                        )
                        
                        # Afficher les détails du consultant sélectionné
                        if consultant_to_add:
                            col_info1, col_info2 = st.columns(2)
                            with col_info1:
                                st.write(f"**Email:** {consultant_to_add.email}")
                                st.write(f"**Grade:** {getattr(consultant_to_add, 'grade', 'Non défini')}")
                            with col_info2:
                                current_practice = "Aucune"
                                if consultant_to_add.practice_id:
                                    current_practice_obj = PracticeService.get_practice_by_id(consultant_to_add.practice_id)
                                    if current_practice_obj:
                                        current_practice = current_practice_obj.nom
                                st.write(f"**Practice actuelle:** {current_practice}")
                                st.write(f"**Salaire:** {getattr(consultant_to_add, 'salaire_actuel', 0):,.0f}€")
                        
                        if st.button("➕ Affecter à la practice", key="add_consultant"):
                            try:
                                success = PracticeService.assign_consultant_to_practice(
                                    consultant_to_add.id, selected_practice.id
                                )
                                if success:
                                    st.success(f"✅ {consultant_to_add.prenom} {consultant_to_add.nom} a été affecté à la practice {selected_practice.nom}")
                                    st.rerun()
                                else:
                                    st.error("❌ Erreur lors de l'affectation du consultant")
                            except Exception as e:
                                st.error(f"❌ Erreur: {e}")
                    else:
                        st.info("Tous les consultants sont déjà affectés à cette practice.")
                
                with tab3:
                    # Actions supplémentaires
                    st.write("**Actions sur la practice:**")
                    
                    col_action1, col_action2 = st.columns(2)
                    
                    with col_action1:
                        st.write("**Statistiques de la practice:**")
                        try:
                            stats = PracticeService.get_practice_statistics()
                            practice_stats = next(
                                (p for p in stats.get("practices_detail", []) 
                                 if p["nom"] == selected_practice.nom), 
                                None
                            )
                            if practice_stats:
                                st.metric("Total consultants", practice_stats["total_consultants"])
                                st.metric("Consultants actifs", practice_stats["consultants_actifs"])
                                st.write(f"**Responsable:** {practice_stats['responsable']}")
                        except Exception as e:
                            st.error(f"Erreur lors du chargement des statistiques: {e}")
                    
                    with col_action2:
                        st.write("**Export des données:**")
                        if st.button("📊 Exporter la liste (CSV)", key="export_csv"):
                            try:
                                consultants_dict = PracticeService.get_consultants_by_practice(selected_practice.id)
                                if consultants_dict and pd is not None:
                                    practice_name = list(consultants_dict.keys())[0]
                                    consultants = consultants_dict[practice_name]
                                    
                                    if consultants:
                                        export_data = []
                                        for consultant in consultants:
                                            export_data.append({
                                                "ID": consultant.id,
                                                "Nom": consultant.nom,
                                                "Prénom": consultant.prenom,
                                                "Email": consultant.email,
                                                "Grade": getattr(consultant, 'grade', ''),
                                                "Disponible": getattr(consultant, 'disponibilite', False),
                                                "Salaire": getattr(consultant, 'salaire_actuel', 0),
                                                "Practice": selected_practice.nom
                                            })
                                        
                                        df_export = pd.DataFrame(export_data)
                                        csv = df_export.to_csv(index=False)
                                        
                                        st.download_button(
                                            label="💾 Télécharger CSV",
                                            data=csv,
                                            file_name=f"consultants_{selected_practice.nom.replace(' ', '_')}.csv",
                                            mime="text/csv"
                                        )
                                        st.success("✅ Export prêt au téléchargement!")
                            except Exception as e:
                                st.error(f"❌ Erreur lors de l'export: {e}")
        else:
            st.warning("Aucune practice trouvée.")

    except Exception as e:
        st.error(f"Erreur lors du chargement des consultants: {e}")
        st.exception(e)


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
