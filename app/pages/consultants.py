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

def show():
    """Affiche la page de gestion des consultants"""
    
    st.title("👥 Gestion des consultants")
    st.markdown("### Gérez les profils de vos consultants")
    
    # Onglets pour organiser les fonctionnalités
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Liste des consultants", "➕ Ajouter un consultant", "✏️ Modifier un consultant", "📄 Import CV"])
    
    with tab1:
        show_consultants_list()
    
    with tab2:
        show_add_consultant_form()
    
    with tab3:
        show_edit_consultant_form()
    
    with tab4:
        show_cv_import()

def show_consultants_list():
    """Affiche la liste des consultants avec options de filtrage"""
    
    st.subheader("📋 Liste des consultants")
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    
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
            
            # Afficher le tableau
            if not df.empty:
                st.dataframe(
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
                    }
                )
                
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
                
                # Actions rapides par consultant
                st.markdown("---")
                st.subheader("⚡ Actions rapides")
                
                selected_consultant = st.selectbox(
                    "Sélectionner un consultant pour les actions",
                    options=df['Prénom'] + " " + df['Nom'],  # Changé: Prénom + Nom au lieu de Nom + Prénom
                    index=0
                )
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("✏️ Modifier"):
                        consultant_id = df[df['Prénom'] + " " + df['Nom'] == selected_consultant]['ID'].iloc[0]
                        st.session_state.edit_consultant_id = consultant_id
                        st.success(f"✏️ Consultant sélectionné pour modification. Allez dans l'onglet 'Modifier un consultant'")
                
                with col2:
                    if st.button("🎯 Voir compétences"):
                        st.info(f"🎯 Compétences de {selected_consultant} - Redirection vers page compétences !")
                
                with col3:
                    if st.button("💼 Voir missions"):
                        st.info(f"💼 Missions de {selected_consultant} - Redirection vers page missions !")
                
                with col4:
                    if st.button("🗑️ Supprimer", type="secondary"):
                        try:
                            # Recherche plus robuste de l'ID
                            matching_rows = df[df['Prénom'] + " " + df['Nom'] == selected_consultant]
                            
                            if matching_rows.empty:
                                st.error(f"❌ Consultant '{selected_consultant}' non trouvé dans la liste")
                                st.write("Debug - Consultants disponibles:")
                                st.write(df[['ID', 'Prénom', 'Nom']])
                                return
                            
                            consultant_id = int(matching_rows['ID'].iloc[0])
                            st.info(f"🔍 Debug: ID trouvé = {consultant_id} pour '{selected_consultant}'")
                            
                            # Clé unique pour la confirmation de suppression
                            confirm_key = f"confirm_delete_{consultant_id}"
                            
                            if not st.session_state.get(confirm_key, False):
                                st.session_state[confirm_key] = True
                                st.warning(f"⚠️ Confirmez-vous la suppression de {selected_consultant} (ID: {consultant_id}) ? Cliquez à nouveau pour confirmer.")
                            else:
                                try:
                                    st.info(f"🔄 Tentative de suppression du consultant ID {consultant_id}...")
                                    result = ConsultantService.delete_consultant(consultant_id)
                                    
                                    if result:
                                        st.success(f"✅ {selected_consultant} supprimé avec succès !")
                                        # Nettoyer toutes les confirmations
                                        keys_to_remove = [key for key in st.session_state.keys() if key.startswith('confirm_delete_')]
                                        for key in keys_to_remove:
                                            del st.session_state[key]
                                        if 'edit_consultant_id' in st.session_state:
                                            del st.session_state['edit_consultant_id']
                                        st.rerun()
                                    else:
                                        st.error(f"❌ Échec de la suppression de {selected_consultant} (ID: {consultant_id})")
                                        st.session_state[confirm_key] = False
                                        
                                except Exception as delete_error:
                                    st.error(f"❌ Erreur lors de la suppression: {str(delete_error)}")
                                    st.session_state[confirm_key] = False
                                    
                        except Exception as e:
                            st.error(f"❌ Erreur dans la logique de suppression: {str(e)}")
                            st.write(f"Debug - Exception type: {type(e).__name__}")
                            st.write(f"Debug - Selected consultant: '{selected_consultant}'")
                            import traceback
                            st.code(traceback.format_exc())
            
            else:
                st.info("Aucun consultant ne correspond aux critères de recherche.")
        
        else:
            st.info("📝 Aucun consultant enregistré. Commencez par ajouter votre premier consultant !")
            if st.button("➕ Ajouter le premier consultant"):
                st.switch_page("Consultants")
    
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des consultants: {e}")
        st.info("🔧 Vérifiez que la base de données est initialisée.")

def show_add_consultant_form():
    """Affiche le formulaire d'ajout de consultant"""
    
    st.subheader("➕ Ajouter un nouveau consultant")
    
    with st.form("add_consultant_form"):
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
                    
                    # Afficher un aperçu des données saisies
                    with st.expander("👁️ Aperçu des données"):
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
                    
                    # Suggérer de voir la liste
                    st.info("💡 Consultez l'onglet 'Liste des consultants' pour voir votre nouveau consultant !")
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
    
    # Sélection du consultant à modifier
    consultants = ConsultantService.get_all_consultants()
    
    if not consultants:
        st.info("📝 Aucun consultant à modifier. Ajoutez d'abord des consultants.")
        return
    
    # Options pour le selectbox
    consultant_options = {}
    for consultant in consultants:
        key = f"{consultant.prenom} {consultant.nom} ({consultant.email})"
        consultant_options[key] = consultant
    
    # Pré-sélection si un consultant a été choisi depuis la liste
    selected_key = None
    if 'edit_consultant_id' in st.session_state:
        for key, consultant in consultant_options.items():
            if consultant.id == st.session_state.edit_consultant_id:
                selected_key = key
                break
    
    selected_consultant_key = st.selectbox(
        "👤 Sélectionner le consultant à modifier",
        options=list(consultant_options.keys()),
        index=list(consultant_options.keys()).index(selected_key) if selected_key else 0
    )
    
    consultant = consultant_options[selected_consultant_key]
    
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
                    
                    st.info("💡 Les modifications ont été sauvegardées. Consultez la liste pour voir les changements.")
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

if __name__ == "__main__":
    show()
