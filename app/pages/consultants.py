"""
Page de gestion des consultants
CRUD complet pour les consultants avec formulaires et tableaux
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Import des modèles et services
sys.path.append(os.path.dirname(__file__))
from app.services.consultant_service import ConsultantService

def clear_cache_and_refresh(keep_edit_id=False):
    """Nettoie le cache et force le rafraîchissement des données"""
    # Nettoyer le cache Streamlit
    st.cache_data.clear()
    
    # Nettoyer les états de session liés aux sélections
    keys_to_clear = [
        'selected_consultant_id', 
        'selected_consultant_name', 
        'show_delete_dialog'
    ]
    
    # Ajouter edit_consultant_id à la liste seulement si on ne veut pas le garder
    if not keep_edit_id:
        keys_to_clear.append('edit_consultant_id')
    
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

def show():
    """Affiche la page de gestion des consultants"""
    
    st.title("👥 Gestion des consultants")
    st.markdown("### Gérez les profils de vos consultants")
    
    # Onglets pour organiser les fonctionnalités
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Liste des consultants", "➕ Ajouter un consultant", "✏️ Modifier un consultant", "�️ Supprimer un consultant", "�📄 Import CV"])
    
    with tab1:
        show_consultants_list()
    
    with tab2:
        show_add_consultant_form()
    
    with tab3:
        show_edit_consultant_form()
    
    with tab4:
        show_delete_consultant_form()
    
    with tab5:
        show_cv_import()

def show_consultants_list():
    """Affiche la liste des consultants avec options de filtrage"""
    
    st.subheader("📋 Liste des consultants")
    
    # Vérifier si un consultant vient d'être ajouté
    if 'newly_added_consultant' in st.session_state:
        consultant_name = st.session_state.newly_added_consultant
        st.success(f"🎉 **Nouveau consultant ajouté** : {consultant_name}")
        del st.session_state.newly_added_consultant
    
    # Filtres et bouton de rafraîchissement
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        search_name = st.text_input("🔍 Rechercher par nom", placeholder="Nom ou prénom...")
    
    with col2:
        filter_availability = st.selectbox(
            "📊 Disponibilité",
            ["Tous", "Disponible", "En mission"]
        )
    
    with col3:
        sort_by = st.selectbox(
            "📈 Trier par",
            ["Nom", "Date d'ajout", "Dernière mise à jour"]
        )
    
    with col4:
        st.write("")  # Espacement
        if st.button("🔄", help="Actualiser la liste", key="refresh_consultants"):
            clear_cache_and_refresh(keep_edit_id=True)
            st.rerun()
    
    # Récupérer les consultants depuis la base de données
    try:
        if search_name:
            consultants = ConsultantService.search_consultants(search_name)
        else:
            consultants = ConsultantService.get_all_consultants()
        
        if consultants:
            # Convertir en DataFrame pour l'affichage
            consultants_data = []
            for consultant in consultants:
                consultants_data.append({
                    "ID": consultant.id,
                    "Nom": consultant.nom,
                    "Prénom": consultant.prenom,
                    "Email": consultant.email,
                    "Téléphone": consultant.telephone or "-",
                    "Salaire": consultant.salaire_actuel or 0,
                    "Disponibilité": "✅ Disponible" if consultant.disponibilite else "🔴 En mission",
                    "Dernière MAJ": consultant.derniere_maj.strftime("%Y-%m-%d") if consultant.derniere_maj else "-"
                })
            
            df = pd.DataFrame(consultants_data)
            
            # Appliquer le filtre de disponibilité
            if filter_availability != "Tous":
                status = "✅ Disponible" if filter_availability == "Disponible" else "🔴 En mission"
                df = df[df['Disponibilité'] == status]
            
            # Afficher le tableau avec sélection
            if not df.empty:
                event = st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Salaire": st.column_config.NumberColumn(
                            "Salaire (€)",
                            format="€%d"
                        ),
                        "Email": st.column_config.TextColumn(
                            "Email",
                            width="medium"
                        )
                    },
                    on_select="rerun",
                    selection_mode="single-row",
                    key="consultants_table"
                )
                
                # Vérifier si une ligne est sélectionnée
                if event.selection.rows:
                    selected_row_index = event.selection.rows[0]
                    selected_consultant = df.iloc[selected_row_index]
                    
                    # Stocker les données du consultant sélectionné
                    st.session_state.selected_consultant_id = int(selected_consultant['ID'])
                    st.session_state.selected_consultant_name = f"{selected_consultant['Prénom']} {selected_consultant['Nom']}"
                    
                    # NOUVEAU : Définir automatiquement l'ID pour la modification
                    st.session_state.edit_consultant_id = int(selected_consultant['ID'])
                    
                    st.info(f"👤 Consultant sélectionné: **{selected_consultant['Prénom']} {selected_consultant['Nom']}**")
                    st.success(f"✏️ Prêt pour modification - Allez dans l'onglet 'Modifier un consultant'")
                else:
                    st.info("👆 Cliquez sur une ligne du tableau pour sélectionner un consultant")
                
                # Actions en lot
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📤 Exporter en CSV"):
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Télécharger CSV",
                            data=csv,
                            file_name=f"consultants_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                
                with col2:
                    if st.button("📊 Générer rapport"):
                        st.info("📊 Génération de rapport - Fonctionnalité à venir !")
                
                with col3:
                    if st.button("✉️ Email groupé"):
                        st.info("✉️ Email groupé - Fonctionnalité à venir !")
            
            else:
                st.info("Aucun consultant ne correspond aux critères de recherche.")
        
        else:
            st.info("📝 Aucun consultant enregistré. Utilisez l'onglet 'Ajouter un consultant' pour commencer !")
    
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des consultants: {e}")
        st.info("🔧 Vérifiez que la base de données est initialisée.")

def show_add_consultant_form():
    """Affiche le formulaire d'ajout de consultant"""
    
    st.subheader("➕ Ajouter un nouveau consultant")
    
    # Générer une clé unique pour le formulaire pour forcer la réinitialisation
    form_key = f"add_consultant_form_{st.session_state.get('form_reset_counter', 0)}"
    
    with st.form(form_key):
        col1, col2 = st.columns(2)
        
        with col1:
            prenom = st.text_input("Prénom *", placeholder="Ex: Jean")
            email = st.text_input("Email *", placeholder="jean.dupont@example.com")
            salaire = st.number_input("Salaire annuel (€)", min_value=0, value=45000, step=1000)
        
        with col2:
            nom = st.text_input("Nom *", placeholder="Ex: Dupont")
            telephone = st.text_input("Téléphone", placeholder="01.23.45.67.89")
            disponible = st.checkbox("Disponible", value=True)
        
        notes = st.text_area("Notes", placeholder="Informations complémentaires...")
        
        # Boutons du formulaire
        col1, col2, col3 = st.columns(3)
        
        with col1:
            submitted = st.form_submit_button("✅ Ajouter le consultant", type="primary")
        
        with col2:
            reset = st.form_submit_button("🔄 Réinitialiser")
        
        with col3:
            preview = st.form_submit_button("👁️ Aperçu")
        
        if submitted:
            # Validation des champs obligatoires
            if not prenom or not nom or not email:
                st.error("❌ Veuillez remplir tous les champs obligatoires (Prénom, Nom, Email)")
            else:
                # Préparer les données
                consultant_data = {
                    'prenom': prenom,
                    'nom': nom,
                    'email': email,
                    'telephone': telephone,
                    'salaire': salaire,
                    'disponible': disponible,
                    'notes': notes
                }
                
                # Sauvegarder en base de données
                if ConsultantService.create_consultant(consultant_data):
                    st.success(f"✅ Consultant {prenom} {nom} ajouté avec succès !")
                    st.balloons()
                    
                    # Nettoyer le cache pour rafraîchir les données
                    clear_cache_and_refresh()
                    
                    # Afficher un aperçu des données saisies
                    with st.expander("👁️ Aperçu des données ajoutées"):
                        st.json({
                            "prenom": prenom,
                            "nom": nom,
                            "email": email,
                            "telephone": telephone,
                            "salaire": salaire,
                            "disponible": disponible,
                            "notes": notes,
                            "date_creation": datetime.now().isoformat()
                        })
                    
                    # Redirection automatique vers la liste des consultants
                    st.info("� Redirection automatique vers la liste des consultants...")
                    
                    # Stocker le consultant ajouté pour le mettre en évidence
                    st.session_state.newly_added_consultant = f"{prenom} {nom}"
                    
                    # Incrémenter le compteur pour forcer la réinitialisation du formulaire
                    st.session_state.form_reset_counter = st.session_state.get('form_reset_counter', 0) + 1
                    
                    st.info("🔄 Consultant ajouté ! Allez voir la liste des consultants pour le retrouver.")
                    st.success("📝 Le formulaire est maintenant réinitialisé pour un nouvel ajout.")
                    
                    # Réinitialiser le formulaire en rechargeant la page
                    import time
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de l'ajout du consultant. Vérifiez la base de données.")
        
        if reset:
            st.rerun()
        
        if preview:
            st.info("👁️ Aperçu des données à sauvegarder")
            preview_data = {
                "Prénom": prenom,
                "Nom": nom,
                "Email": email,
                "Téléphone": telephone,
                "Salaire": f"{salaire}€",
                "Disponible": "Oui" if disponible else "Non",
                "Notes": notes or "Aucune"
            }
            st.table(preview_data)

def show_edit_consultant_form():
    """Affiche le formulaire de modification d'un consultant"""
    
    st.subheader("✏️ Modifier un consultant")
    
    # Debug: Afficher l'état de la session
    if st.checkbox("🔍 Debug: Voir l'état de la session", key="debug_session"):
        st.write("Session state:", dict(st.session_state))
    
    # Vérifier si un consultant a été sélectionné depuis la liste
    if 'edit_consultant_id' in st.session_state:
        # Récupérer le consultant sélectionné
        try:
            consultant_id = st.session_state.edit_consultant_id
            st.success(f"🎯 **ID consultant détecté**: {consultant_id}")
            
            consultant = ConsultantService.get_consultant_by_id(consultant_id)
            if not consultant:
                st.error("❌ Consultant introuvable")
                del st.session_state.edit_consultant_id
                return
                
            st.success(f"✏️ **Consultant sélectionné depuis la liste**: {consultant.prenom} {consultant.nom}")
            
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement: {e}")
            del st.session_state.edit_consultant_id
            return
    else:
        st.warning("⚠️ Aucun consultant pré-sélectionné")
        # Sélection manuelle du consultant
        consultants = ConsultantService.get_all_consultants()
        
        if not consultants:
            st.info("📝 Aucun consultant à modifier. Ajoutez d'abord des consultants.")
            return
        
        # Options pour le selectbox
        consultant_options = {}
        for cons in consultants:
            key = f"{cons.prenom} {cons.nom} ({cons.email})"
            consultant_options[key] = cons
        
        selected_consultant_key = st.selectbox(
            "👤 Sélectionner le consultant à modifier",
            options=list(consultant_options.keys()),
            index=0
        )
        
        consultant = consultant_options[selected_consultant_key]
        st.info("💡 **Conseil**: Vous pouvez aussi sélectionner un consultant dans la 'Liste des consultants' puis cliquer sur 'Modifier'")
    
    st.info(f"📝 Modification de: **{consultant.prenom} {consultant.nom}**")
    
    with st.form("edit_consultant_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            prenom = st.text_input("Prénom *", value=consultant.prenom)
            email = st.text_input("Email *", value=consultant.email)
            salaire = st.number_input("Salaire annuel (€)", min_value=0, value=int(consultant.salaire_actuel or 0), step=1000)
        
        with col2:
            nom = st.text_input("Nom *", value=consultant.nom)
            telephone = st.text_input("Téléphone", value=consultant.telephone or "")
            disponible = st.checkbox("Disponible", value=consultant.disponibilite)
        
        notes = st.text_area("Notes", value=consultant.notes or "")
        
        # Boutons du formulaire
        col1, col2, col3 = st.columns(3)
        
        with col1:
            submitted = st.form_submit_button("✅ Mettre à jour", type="primary")
        
        with col2:
            cancel = st.form_submit_button("❌ Annuler")
        
        with col3:
            preview = st.form_submit_button("👁️ Aperçu")
        
        if submitted:
            # Validation des champs obligatoires
            if not prenom or not nom or not email:
                st.error("❌ Veuillez remplir tous les champs obligatoires (Prénom, Nom, Email)")
            else:
                # Préparer les données de mise à jour
                update_data = {
                    'prenom': prenom,
                    'nom': nom,
                    'email': email,
                    'telephone': telephone,
                    'salaire_actuel': salaire,
                    'disponibilite': disponible,
                    'notes': notes
                }
                
                # Mettre à jour en base de données
                if ConsultantService.update_consultant(consultant.id, update_data):
                    st.success(f"✅ Consultant {prenom} {nom} mis à jour avec succès !")
                    st.balloons()
                    
                    # Supprimer la sélection de la session
                    if 'edit_consultant_id' in st.session_state:
                        del st.session_state.edit_consultant_id
                    
                    st.info("� Retour automatique à la liste des consultants...")
                    
                    # Forcer le rafraîchissement et retourner à la liste
                    import time
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de la mise à jour du consultant.")
        
        if cancel:
            if 'edit_consultant_id' in st.session_state:
                del st.session_state.edit_consultant_id
            st.info("❌ Modification annulée")
            st.rerun()
        
        if preview:
            st.info("👁️ Aperçu des modifications")
            changes = {}
            if prenom != consultant.prenom:
                changes["Prénom"] = f"{consultant.prenom} → {prenom}"
            if nom != consultant.nom:
                changes["Nom"] = f"{consultant.nom} → {nom}"
            if email != consultant.email:
                changes["Email"] = f"{consultant.email} → {email}"
            if telephone != (consultant.telephone or ""):
                changes["Téléphone"] = f"{consultant.telephone or 'Vide'} → {telephone or 'Vide'}"
            if salaire != int(consultant.salaire_actuel or 0):
                changes["Salaire"] = f"{consultant.salaire_actuel or 0}€ → {salaire}€"
            if disponible != consultant.disponibilite:
                changes["Disponibilité"] = f"{'Oui' if consultant.disponibilite else 'Non'} → {'Oui' if disponible else 'Non'}"
            if notes != (consultant.notes or ""):
                changes["Notes"] = f"{'Modifiées' if notes != (consultant.notes or '') else 'Inchangées'}"
            
            if changes:
                st.table(changes)
            else:
                st.info("Aucune modification détectée")

def show_cv_import():
    """Affiche la section d'import de CV"""
    
    st.subheader("📄 Import et analyse de CV")
    st.markdown("Uploadez des CVs pour extraire automatiquement les compétences et expériences.")
    
    # Sélection du consultant
    consultant_options = ["Jean Dupont", "Marie Martin", "Pierre Bernard"]  # TODO: Récupérer de la DB
    selected_consultant = st.selectbox(
        "👤 Sélectionner le consultant",
        consultant_options
    )
    
    # Upload de fichier
    uploaded_file = st.file_uploader(
        "📎 Choisir un fichier CV",
        type=['pdf', 'docx', 'doc'],
        help="Formats supportés: PDF, Word (DOCX, DOC)"
    )
    
    if uploaded_file is not None:
        st.success(f"📄 Fichier '{uploaded_file.name}' uploadé avec succès !")
        
        # Informations sur le fichier
        file_details = {
            "Nom du fichier": uploaded_file.name,
            "Taille": f"{uploaded_file.size / 1024:.1f} KB",
            "Type": uploaded_file.type
        }
        st.table(file_details)
        
        # Simulation du parsing
        with st.spinner("🔄 Analyse du CV en cours..."):
            import time
            time.sleep(2)  # Simulation du traitement
        
        # Résultats de l'analyse (simulation)
        st.subheader("🎯 Compétences détectées")
        
        detected_skills = [
            {"Compétence": "Python", "Expérience": "5 ans", "Confiance": "95%"},
            {"Compétence": "Machine Learning", "Expérience": "3 ans", "Confiance": "88%"},
            {"Compétence": "SQL", "Expérience": "4 ans", "Confiance": "92%"},
            {"Compétence": "Docker", "Expérience": "2 ans", "Confiance": "78%"},
        ]
        
        df_skills = pd.DataFrame(detected_skills)
        st.dataframe(df_skills, use_container_width=True, hide_index=True)
        
        # Actions sur les compétences détectées
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Valider toutes les compétences"):
                st.success("✅ Compétences ajoutées au profil du consultant !")
        
        with col2:
            if st.button("🔍 Réviser manuellement"):
                st.info("🔍 Redirection vers la page de gestion des compétences...")
        
        # Contenu extrait (aperçu)
        with st.expander("📄 Contenu extrait du CV"):
            st.text_area(
                "Texte extrait",
                value="Jean Dupont\nData Scientist Senior\n\nExpérience:\n- 5 ans en Python et Machine Learning\n- Projets d'analyse prédictive\n- Maîtrise de SQL et bases de données\n...",
                height=200,
                disabled=True
            )

def show_delete_consultant_form():
    """Affiche le formulaire de suppression d'un consultant"""
    
    st.subheader("🗑️ Supprimer un consultant")
    
    # Vérifier si un consultant a été sélectionné depuis la liste
    if 'selected_consultant_id' in st.session_state and 'selected_consultant_name' in st.session_state:
        # Récupérer le consultant sélectionné
        try:
            consultant_id = st.session_state.selected_consultant_id
            consultant_name = st.session_state.selected_consultant_name
            
            consultant = ConsultantService.get_consultant_by_id(consultant_id)
            if not consultant:
                st.error("❌ Consultant introuvable")
                del st.session_state.selected_consultant_id
                del st.session_state.selected_consultant_name
                return
                
            st.success(f"🎯 **Consultant sélectionné depuis la liste**: {consultant_name}")
            
            # Dialog de confirmation immédiat - Workflow simplifié
            st.error(f"### ⚠️ CONFIRMER LA SUPPRESSION")
            st.error(f"**Voulez-vous vraiment supprimer {consultant.prenom} {consultant.nom} ?**")
            
            # Informations résumées du consultant
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"📧 **Email**: {consultant.email}")
                st.write(f"💰 **Salaire**: {consultant.salaire_actuel or 0}€")
            with col2:
                st.write(f"📞 **Téléphone**: {consultant.telephone or 'Non renseigné'}")
                st.write(f"✅ **Disponible**: {'Oui' if consultant.disponibilite else 'Non'}")
            
            st.warning("⚠️ Cette action est **IRRÉVERSIBLE** et supprimera toutes les données associées.")
            
            # Boutons de confirmation - Workflow direct
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("✅ OUI, SUPPRIMER", type="primary", key="confirm_delete"):
                    try:
                        result = ConsultantService.delete_consultant(consultant_id)
                        
                        if result:
                            st.success(f"✅ {consultant.prenom} {consultant.nom} a été supprimé avec succès !")
                            st.balloons()
                            
                            # Nettoyer tous les états
                            keys_to_clean = ['selected_consultant_id', 'selected_consultant_name', 'edit_consultant_id']
                            for key in keys_to_clean:
                                if key in st.session_state:
                                    del st.session_state[key]
                            
                            # Nettoyer le cache et rafraîchir
                            clear_cache_and_refresh()
                            
                            # Attendre un peu puis recharger
                            import time
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Erreur lors de la suppression du consultant.")
                    except Exception as e:
                        st.error(f"❌ Erreur technique: {str(e)}")
            
            with col2:
                if st.button("❌ NON, ANNULER", key="cancel_delete"):
                    # Nettoyer les sélections
                    if 'selected_consultant_id' in st.session_state:
                        del st.session_state.selected_consultant_id
                    if 'selected_consultant_name' in st.session_state:
                        del st.session_state.selected_consultant_name
                    st.info("❌ Suppression annulée")
                    st.rerun()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**👤 Prénom**: {consultant.prenom}")
                st.write(f"**👤 Nom**: {consultant.nom}")
                st.write(f"**📧 Email**: {consultant.email}")
                st.write(f"**� Téléphone**: {consultant.telephone or 'Non renseigné'}")
            
            with col2:
                st.write(f"**💰 Salaire**: {consultant.salaire_actuel or 0}€")
                st.write(f"**✅ Disponible**: {'Oui' if consultant.disponibilite else 'Non'}")
                st.write(f"**📅 Créé le**: {consultant.date_creation.strftime('%d/%m/%Y') if consultant.date_creation else 'N/A'}")
                st.write(f"**� Modifié le**: {consultant.derniere_maj.strftime('%d/%m/%Y') if consultant.derniere_maj else 'N/A'}")
            
            if consultant.notes:
                st.write(f"**📝 Notes**: {consultant.notes}")
            
            # Bouton de suppression principal
            st.markdown("---")
            st.warning("⚠️ **Attention**: Cette action supprimera définitivement le consultant et toutes ses données associées (compétences, missions, CV).")
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("🗑️ SUPPRIMER CE CONSULTANT", type="primary"):
                    st.session_state.show_delete_confirmation = True
            
            with col2:
                if st.button("❌ Annuler"):
                    # Nettoyer les sélections
                    if 'selected_consultant_id' in st.session_state:
                        del st.session_state.selected_consultant_id
                    if 'selected_consultant_name' in st.session_state:
                        del st.session_state.selected_consultant_name
                    st.info("❌ Suppression annulée")
                    st.rerun()
            
            # Dialog de confirmation
            if st.session_state.get("show_delete_confirmation", False):
                st.markdown("---")
                st.error(f"### ⚠️ CONFIRMATION DE SUPPRESSION")
                st.error(f"**Êtes-vous absolument sûr de vouloir supprimer {consultant.prenom} {consultant.nom} ?**")
                st.warning("Cette action est **IRRÉVERSIBLE** et supprimera :")
                st.markdown("""
                - ✖️ Le profil du consultant
                - ✖️ Toutes ses compétences
                - ✖️ Toutes ses missions
                - ✖️ Tous ses CVs uploadés
                """)
                
                # Debug: Afficher l'état
                st.write("🔍 Debug:", {
                    "consultant_id": consultant_id,
                    "consultant_name": consultant_name,
                    "session_state_keys": list(st.session_state.keys())
                })
                
                col1, col2 = st.columns(2)
                
                with col1:
                    confirm_clicked = st.button("✅ OUI, SUPPRIMER DÉFINITIVEMENT", type="primary", key="final_delete_confirm")
                    if confirm_clicked:
                        st.write("🔍 Bouton de confirmation cliqué !")
                        try:
                            st.write(f"🔍 Tentative de suppression du consultant ID: {consultant_id}")
                            result = ConsultantService.delete_consultant(consultant_id)
                            st.write(f"🔍 Résultat de la suppression: {result}")
                            
                            if result:
                                st.success(f"✅ {consultant.prenom} {consultant.nom} a été supprimé avec succès !")
                                st.balloons()
                                
                                # Nettoyer tous les états
                                keys_to_clean = ['selected_consultant_id', 'selected_consultant_name', 'show_delete_confirmation', 'edit_consultant_id']
                                for key in keys_to_clean:
                                    if key in st.session_state:
                                        del st.session_state[key]
                                
                                # Nettoyer le cache
                                st.cache_data.clear()
                                
                                st.info("🔄 Retour automatique à la liste des consultants...")
                                
                                # Attendre un peu puis recharger
                                import time
                                time.sleep(1.5)
                                st.rerun()
                            else:
                                st.error("❌ Erreur lors de la suppression du consultant.")
                                st.session_state.show_delete_confirmation = False
                        except Exception as e:
                            st.error(f"❌ Erreur technique: {str(e)}")
                            st.session_state.show_delete_confirmation = False
                
                with col2:
                    cancel_clicked = st.button("❌ NON, ANNULER", key="cancel_final_delete")
                    if cancel_clicked:
                        st.write("🔍 Bouton d'annulation cliqué !")
                        st.session_state.show_delete_confirmation = False
                        st.info("❌ Suppression annulée")
                        st.rerun()
            
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement: {e}")
            # Nettoyer les états en cas d'erreur
            if 'selected_consultant_id' in st.session_state:
                del st.session_state.selected_consultant_id
            if 'selected_consultant_name' in st.session_state:
                del st.session_state.selected_consultant_name
            return
    
    else:
        # Aucun consultant sélectionné
        st.warning("⚠️ Aucun consultant sélectionné")
        
        st.info("""
        **Workflow de suppression simplifié :**
        
        1. 📋 Allez dans l'onglet **'Liste des consultants'**
        2. 👆 **Cliquez sur une ligne** du tableau pour sélectionner un consultant
        3. 🗑️ **Revenez dans cet onglet** → Confirmation immédiate
        4. ✅ **Cliquez sur "OUI, SUPPRIMER"** → Suppression terminée !
        
        ➡️ Sélectionnez d'abord un consultant dans la liste !
        """)
        
        st.markdown("---")
        
        # Afficher un aperçu des consultants disponibles
        consultants = ConsultantService.get_all_consultants()
        
        if consultants:
            st.subheader("📊 Consultants disponibles pour suppression")
            
            consultant_info = []
            for consultant in consultants:
                consultant_info.append({
                    "Prénom": consultant.prenom,
                    "Nom": consultant.nom,
                    "Email": consultant.email,
                    "Disponible": "✅" if consultant.disponibilite else "❌"
                })
            
            df_info = pd.DataFrame(consultant_info)
            st.dataframe(df_info, use_container_width=True, hide_index=True)
            
            st.info(f"📈 **Total**: {len(consultants)} consultant(s) dans la base de données")
        else:
            st.warning("📝 Aucun consultant dans la base de données.")
        
        st.markdown("---")
        st.success("💡 **Conseil**: Sélectionnez un consultant dans la 'Liste des consultants' puis revenez ici")

if __name__ == "__main__":
    show()
