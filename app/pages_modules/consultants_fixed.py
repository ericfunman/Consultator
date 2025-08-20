"""
Page de gestion des consultants
CRUD complet pour les consultants avec formulaires, tableaux et gestion de documents
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os
import platform
import subprocess

# Import des modèles et services
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from services.consultant_service import ConsultantService
from services.document_analyzer import DocumentAnalyzer
from services.technology_service import TechnologyService
from components.technology_widget import technology_multiselect
from database.database import get_database_session
from database.models import Mission, ConsultantCompetence, Competence

def show():
    """Affiche la page de gestion des consultants"""
    
    st.title("👥 Gestion des consultants")
    st.markdown("### Gérez les profils de vos consultants")
    
    # Vérifier si on doit afficher le profil d'un consultant spécifique
    if 'view_consultant_profile' in st.session_state:
        show_consultant_profile()
        return
    
    # Onglets pour organiser les fonctionnalités
    tab1, tab2 = st.tabs(["📋 Liste des consultants", "➕ Ajouter un consultant"])
    
    with tab1:
        show_consultants_list()
    
    with tab2:
        show_add_consultant_form()

def show_consultant_profile():
    """Affiche le profil détaillé d'un consultant"""
    
    consultant_id = st.session_state.view_consultant_profile
    consultant = ConsultantService.get_consultant_by_id(consultant_id)
    
    if not consultant:
        st.error("❌ Consultant introuvable")
        del st.session_state.view_consultant_profile
        st.rerun()
        return
    
    # En-tête avec bouton retour
    col1, col2 = st.columns([6, 1])
    
    with col1:
        st.title(f"👤 Profil de {consultant.prenom} {consultant.nom}")
    
    with col2:
        if st.button("← Retour", key="back_to_list"):
            del st.session_state.view_consultant_profile
            st.rerun()
    
    st.markdown("---")
    
    # Informations principales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💰 Salaire annuel", f"{consultant.salaire_actuel or 0:,}€", delta=None)
        
    with col2:
        status = "Disponible" if consultant.disponibilite else "En mission"
        st.metric("📊 Statut", status)
        
    with col3:
        creation_date = consultant.date_creation.strftime("%d/%m/%Y") if consultant.date_creation else "N/A"
        st.metric("📅 Membre depuis", creation_date)
    
    st.markdown("---")
    
    # Détails du profil
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Informations", "💼 Compétences", "🚀 Missions", "📄 Documents", "⚙️ Actions"])
    
    with tab1:
        show_consultant_info(consultant)
    
    with tab2:
        show_consultant_skills(consultant)
    
    with tab3:
        show_consultant_missions(consultant)
    
    with tab4:
        show_consultant_documents(consultant)
    
    with tab5:
        show_consultant_actions(consultant)

def show_consultant_missions(consultant):
    """Affiche l'historique des missions du consultant avec édition"""
    
    st.subheader("🚀 Historique des missions")
    
    # Onglets pour organiser les fonctionnalités
    tab1, tab2 = st.tabs(["📋 Missions existantes", "➕ Ajouter une mission"])
    
    with tab1:
        show_existing_missions(consultant)
    
    with tab2:
        show_add_mission_form(consultant)

def show_existing_missions(consultant):
    """Affiche et permet d'éditer les missions existantes"""
    
    # Récupérer les vraies missions depuis la base de données
    try:
        with get_database_session() as session:
            missions_db = session.query(Mission).filter(
                Mission.consultant_id == consultant.id
            ).order_by(Mission.date_debut.desc()).all()
            
    except Exception as e:
        st.error(f"❌ Erreur lors de la récupération des missions: {e}")
        missions_db = []
    
    if missions_db:
        # Métriques des missions
        col1, col2, col3, col4 = st.columns(4)
        
        total_revenus = sum(m.revenus_generes or 0 for m in missions_db)
        missions_terminees = len([m for m in missions_db if m.statut == "terminee"])
        missions_en_cours = len([m for m in missions_db if m.statut == "en_cours"])
        
        with col1:
            st.metric("💰 Revenus totaux", f"{total_revenus:,}€")
        
        with col2:
            st.metric("✅ Missions terminées", missions_terminees)
        
        with col3:
            st.metric("🔄 Missions en cours", missions_en_cours)
        
        with col4:
            st.metric("📊 Total missions", len(missions_db))
        
        st.markdown("---")
        
        # Mode édition
        if st.checkbox("✏️ Mode édition", key="edit_mode"):
            st.info("📝 Mode édition activé - Vous pouvez maintenant modifier les missions")
            
            for i, mission in enumerate(missions_db):
                with st.expander(f"✏️ Éditer: {mission.client} - {mission.role or 'Rôle non défini'}", expanded=False):
                    edit_mission_form(mission, f"edit_{mission.id}")
        else:
            # Affichage normal (lecture seule)
            for i, mission in enumerate(missions_db):
                with st.expander(f"🚀 {mission.client} - {mission.role or 'Rôle non défini'}", expanded=(i == 0)):
                    show_mission_details(mission, i)
    else:
        st.info("📝 Aucune mission enregistrée pour ce consultant")
        st.markdown("💡 Vous pouvez:")
        st.markdown("- Utiliser l'onglet **'Ajouter une mission'** pour créer une mission manuellement")

def show_mission_details(mission, index):
    """Affiche les détails d'une mission en lecture seule"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**🏢 Client**: {mission.client}")
        st.write(f"**👤 Rôle**: {mission.role or 'Non spécifié'}")
        st.write(f"**📅 Début**: {mission.date_debut.strftime('%Y-%m-%d') if mission.date_debut else 'N/A'}")
        st.write(f"**💰 Revenus**: {mission.revenus_generes or 0:,}€")
    
    with col2:
        st.write(f"**📅 Fin**: {mission.date_fin.strftime('%Y-%m-%d') if mission.date_fin else 'En cours'}")
        
        # Statut avec couleur
        if mission.statut == 'terminee':
            st.success("✅ Terminée")
        elif mission.statut == 'en_cours':
            st.info("🔄 En cours")
        else:
            st.warning("⏸️ En pause")
    
    st.write(f"**🛠️ Technologies**: {mission.technologies_utilisees or 'Non spécifiées'}")
    
    # Description de la mission
    if mission.description and mission.description != "Aucune description":
        st.write("**📝 Description**:")
        st.text_area("Description", value=mission.description, height=100, key=f"desc_readonly_{index}", disabled=True, label_visibility="collapsed")

def edit_mission_form(mission, key_prefix):
    """Formulaire d'édition d'une mission existante"""
    
    with st.form(f"edit_mission_form_{key_prefix}"):
        col1, col2 = st.columns(2)
        
        with col1:
            nom_mission = st.text_input("📋 Nom de la mission", value=mission.nom_mission or "", key=f"{key_prefix}_nom")
            client = st.text_input("🏢 Client", value=mission.client or "", key=f"{key_prefix}_client")
            role = st.text_input("👤 Rôle", value=mission.role or "", key=f"{key_prefix}_role")
            revenus = st.number_input("💰 Revenus (€)", value=float(mission.revenus_generes or 0), min_value=0.0, key=f"{key_prefix}_revenus")
        
        with col2:
            date_debut = st.date_input("📅 Date début", value=mission.date_debut if mission.date_debut else None, key=f"{key_prefix}_debut")
            date_fin = st.date_input("📅 Date fin", value=mission.date_fin if mission.date_fin else None, key=f"{key_prefix}_fin")
            statut = st.selectbox("📊 Statut", 
                                ["en_cours", "terminee", "en_pause"], 
                                index=["en_cours", "terminee", "en_pause"].index(mission.statut) if mission.statut in ["en_cours", "terminee", "en_pause"] else 0,
                                key=f"{key_prefix}_statut")
        
        technologies = technology_multiselect(
            label="🛠️ Technologies",
            key=f"{key_prefix}_tech",
            default_values=mission.technologies_utilisees.split(", ") if mission.technologies_utilisees else []
        )
        description = st.text_area("📝 Description", value=mission.description or "", height=100, key=f"{key_prefix}_desc")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("💾 Sauvegarder les modifications", type="primary"):
                save_mission_changes(mission.id, {
                    'nom_mission': nom_mission,
                    'client': client,
                    'role': role,
                    'date_debut': date_debut,
                    'date_fin': date_fin,
                    'statut': statut,
                    'revenus_generes': revenus,
                    'technologies_utilisees': technologies,
                    'description': description
                })
        
        with col2:
            if st.form_submit_button("🗑️ Supprimer la mission", type="secondary"):
                delete_mission(mission.id)

def show_add_mission_form(consultant):
    """Formulaire d'ajout d'une nouvelle mission"""
    
    st.markdown("### ➕ Ajouter une nouvelle mission")
    
    with st.form("add_mission_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nom_mission = st.text_input("📋 Nom de la mission", placeholder="Ex: Développement application mobile")
            client = st.text_input("🏢 Client", placeholder="Ex: Société Générale")
            role = st.text_input("👤 Rôle", placeholder="Ex: Lead Developer")
            revenus = st.number_input("💰 Revenus (€)", min_value=0.0, value=0.0)
        
        with col2:
            date_debut = st.date_input("📅 Date début")
            date_fin = st.date_input("📅 Date fin (optionnel)", value=None)
            statut = st.selectbox("📊 Statut", ["en_cours", "terminee", "en_pause"])
        
        technologies_str = technology_multiselect(
            label="🛠️ Technologies",
            key="new_mission_tech",
            default_values=[]
        )
        description = st.text_area("📝 Description", height=100, placeholder="Décrivez les activités réalisées durant cette mission...")
        
        if st.form_submit_button("➕ Ajouter la mission", type="primary"):
            add_new_mission(consultant.id, {
                'nom_mission': nom_mission,
                'client': client,
                'role': role,
                'date_debut': date_debut,
                'date_fin': date_fin,
                'statut': statut,
                'revenus_generes': revenus,
                'technologies_utilisees': technologies_str,
                'description': description
            })

def save_mission_changes(mission_id, mission_data):
    """Sauvegarde les modifications d'une mission"""
    try:
        with get_database_session() as session:
            mission = session.query(Mission).filter(Mission.id == mission_id).first()
            
            if mission:
                # Mettre à jour les champs
                mission.nom_mission = mission_data['nom_mission']
                mission.client = mission_data['client']
                mission.role = mission_data['role']
                mission.date_debut = mission_data['date_debut']
                mission.date_fin = mission_data['date_fin']
                mission.statut = mission_data['statut']
                mission.revenus_generes = mission_data['revenus_generes']
                mission.technologies_utilisees = mission_data['technologies_utilisees']
                mission.description = mission_data['description']
                
                session.commit()
                st.success("✅ Mission mise à jour avec succès !")
                st.rerun()
            else:
                st.error("❌ Mission non trouvée")
                
    except Exception as e:
        st.error(f"❌ Erreur lors de la sauvegarde: {e}")

def delete_mission(mission_id):
    """Supprime une mission"""
    try:
        with get_database_session() as session:
            mission = session.query(Mission).filter(Mission.id == mission_id).first()
            
            if mission:
                session.delete(mission)
                session.commit()
                st.success("✅ Mission supprimée avec succès !")
                st.rerun()
            else:
                st.error("❌ Mission non trouvée")
                
    except Exception as e:
        st.error(f"❌ Erreur lors de la suppression: {e}")

def add_new_mission(consultant_id, mission_data):
    """Ajoute une nouvelle mission"""
    
    if not mission_data['nom_mission'] or not mission_data['client']:
        st.error("❌ Le nom de la mission et le client sont obligatoires")
        return
    
    try:
        with get_database_session() as session:
            nouvelle_mission = Mission(
                consultant_id=consultant_id,
                nom_mission=mission_data['nom_mission'],
                client=mission_data['client'],
                role=mission_data['role'],
                date_debut=mission_data['date_debut'],
                date_fin=mission_data['date_fin'],
                statut=mission_data['statut'],
                revenus_generes=mission_data['revenus_generes'],
                technologies_utilisees=mission_data['technologies_utilisees'],
                description=mission_data['description']
            )
            
            session.add(nouvelle_mission)
            session.commit()
            st.success("✅ Nouvelle mission ajoutée avec succès !")
            st.rerun()
            
    except Exception as e:
        st.error(f"❌ Erreur lors de l'ajout: {e}")

def show_consultant_info(consultant):
    """Affiche et permet la modification des informations de base du consultant"""
    
    st.subheader("📋 Informations personnelles")
    
    # Formulaire toujours actif pour modification directe
    with st.form(f"edit_consultant_info_{consultant.id}"):
        col1, col2 = st.columns(2)
        
        with col1:
            prenom = st.text_input("👤 Prénom *", value=consultant.prenom, placeholder="Ex: Jean")
            email = st.text_input("📧 Email *", value=consultant.email, placeholder="jean.dupont@example.com")
            salaire = st.number_input("💰 Salaire annuel (€)", 
                                    min_value=0, 
                                    value=int(consultant.salaire_actuel or 0), 
                                    step=1000)
        
        with col2:
            nom = st.text_input("👤 Nom *", value=consultant.nom, placeholder="Ex: Dupont")
            telephone = st.text_input("📞 Téléphone", 
                                    value=consultant.telephone or "", 
                                    placeholder="01.23.45.67.89")
            disponibilite = st.checkbox("✅ Disponible", value=consultant.disponibilite)
        
        # Notes
        notes = st.text_area("📝 Notes", 
                            value=consultant.notes or "",
                            height=100,
                            placeholder="Notes sur le consultant...")
        
        # Bouton de sauvegarde centré et visible
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col2:
            submitted = st.form_submit_button("💾 Sauvegarder les modifications", 
                                            use_container_width=True,
                                            type="primary")
        
        if submitted:
            # Validation
            if not prenom or not nom or not email:
                st.error("❌ Veuillez remplir tous les champs obligatoires (*)")
            else:
                # Vérifier l'unicité de l'email (sauf pour le consultant actuel)
                existing_consultant = ConsultantService.get_consultant_by_email(email)
                if existing_consultant and existing_consultant.id != consultant.id:
                    st.error(f"❌ Un consultant avec l'email {email} existe déjà !")
                else:
                    try:
                        # Données de mise à jour
                        update_data = {
                            'prenom': prenom.strip(),
                            'nom': nom.strip(),
                            'email': email.strip().lower(),
                            'telephone': telephone.strip() if telephone else None,
                            'salaire_actuel': salaire,
                            'disponibilite': disponibilite,
                            'notes': notes.strip() if notes else None
                        }
                        
                        # Mettre à jour le consultant
                        ConsultantService.update_consultant(consultant.id, update_data)
                        
                        st.success(f"✅ {prenom} {nom} a été modifié avec succès !")
                        
                        # Actualiser la page de profil
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la modification: {e}")

def show_consultant_skills(consultant):
    """Affiche les compétences du consultant"""
    
    st.subheader("💼 Compétences")
    
    # Simulation de données d'exemple
    skills_data = [
        {"Compétence": "Python", "Niveau": "Expert", "Années d'expérience": 5, "Dernière utilisation": "2024"},
        {"Compétence": "Machine Learning", "Niveau": "Avancé", "Années d'expérience": 3, "Dernière utilisation": "2024"},
        {"Compétence": "SQL", "Niveau": "Expert", "Années d'expérience": 4, "Dernière utilisation": "2024"},
        {"Compétence": "Docker", "Niveau": "Intermédiaire", "Années d'expérience": 2, "Dernière utilisation": "2023"},
    ]
    
    if skills_data:
        # Affichage des compétences sous forme de badges et tableau
        st.write("**🏷️ Badges de compétences**")
        
        cols = st.columns(4)
        for i, skill in enumerate(skills_data):
            with cols[i % 4]:
                level_color = {
                    "Expert": "🟢",
                    "Avancé": "🟡", 
                    "Intermédiaire": "🟠",
                    "Débutant": "🔴"
                }.get(skill["Niveau"], "⚪")
                
                st.markdown(f"""
                <div style="padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 5px; text-align: center;">
                    {level_color} <strong>{skill["Compétence"]}</strong><br>
                    <small>{skill["Niveau"]} • {skill["Années d'expérience"]} ans</small>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.write("**📊 Détail des compétences**")
        
        df_skills = pd.DataFrame(skills_data)
        st.dataframe(df_skills, use_container_width=True, hide_index=True)
    
    else:
        st.info("📝 Aucune compétence enregistrée pour ce consultant")

def show_consultant_documents(consultant):
    """Affiche les documents associés au consultant"""
    
    st.subheader("📄 Documents")
    
    # Simulation de documents par défaut
    documents = [
        {"Type": "CV", "Nom": f"CV_{consultant.prenom}_{consultant.nom}_2024.pdf", "Taille": "245 KB", "Date": "2024-03-15"},
        {"Type": "Contrat", "Nom": "Contrat_freelance_2024.pdf", "Taille": "156 KB", "Date": "2024-01-10"},
        {"Type": "Certificat", "Nom": "Certification_AWS_Solutions_Architect.pdf", "Taille": "98 KB", "Date": "2023-11-20"},
    ]
    
    if documents:
        for doc in documents:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                icon = "📄" if doc["Type"] == "CV" else ("📋" if doc["Type"] == "Contrat" else "🎓")
                st.write(f"{icon} **{doc['Nom']}**")
            
            with col2:
                st.write(f"📏 {doc['Taille']}")
            
            with col3:
                st.write(f"📅 {doc['Date']}")
            
            with col4:
                st.button("👁️", key=f"view_{doc['Nom']}", help="Voir le document")
    
    else:
        st.info("📝 Aucun document associé à ce consultant")

def show_consultant_actions(consultant):
    """Affiche les actions disponibles pour le consultant"""
    
    st.subheader("⚙️ Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔧 Actions rapides")
        if st.button("📧 Envoyer un email", use_container_width=True):
            st.info("💡 Fonctionnalité à venir - Intégration email")
        
        if st.button("📋 Exporter le profil", use_container_width=True):
            st.info("💡 Fonctionnalité à venir - Export PDF/Excel")
        
        if st.button("📊 Générer un rapport", use_container_width=True):
            st.info("💡 Fonctionnalité à venir - Rapport d'activité")
    
    with col2:
        st.markdown("#### 🗑️ Zone de danger")
        if st.button("🗑️ Supprimer le consultant", type="secondary", use_container_width=True):
            st.error("⚠️ Cette action supprimera définitivement toutes les données du consultant !")

def show_consultants_list():
    """Affiche la liste des consultants"""
    
    st.subheader("📋 Liste des consultants")
    
    # Récupérer les consultants
    try:
        consultants = ConsultantService.get_all_consultants()
        
        if consultants:
            # Affichage en cartes
            for consultant in consultants:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    
                    with col1:
                        st.markdown(f"### 👤 {consultant.prenom} {consultant.nom}")
                        st.write(f"📧 {consultant.email}")
                        if consultant.telephone:
                            st.write(f"📞 {consultant.telephone}")
                    
                    with col2:
                        status = "✅ Disponible" if consultant.disponibilite else "🔴 Occupé"
                        st.write(f"**Statut**: {status}")
                        if consultant.salaire_actuel:
                            st.write(f"**Salaire**: {consultant.salaire_actuel:,}€")
                    
                    with col3:
                        if consultant.date_creation:
                            st.write(f"**Créé**: {consultant.date_creation.strftime('%d/%m/%Y')}")
                        # Compter les missions
                        # TODO: Récupérer le vrai nombre de missions
                        st.write("**Missions**: 3")
                    
                    with col4:
                        if st.button("👁️ Voir", key=f"view_{consultant.id}"):
                            st.session_state.view_consultant_profile = consultant.id
                            st.rerun()
                    
                    st.divider()
        
        else:
            st.info("📝 Aucun consultant enregistré")
            st.markdown("💡 Utilisez l'onglet **'Ajouter un consultant'** pour commencer")
    
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des consultants: {e}")

def show_add_consultant_form():
    """Affiche le formulaire d'ajout d'un nouveau consultant"""
    
    st.subheader("➕ Ajouter un nouveau consultant")
    
    with st.form("add_consultant_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            prenom = st.text_input("👤 Prénom *", placeholder="Ex: Jean")
            email = st.text_input("📧 Email *", placeholder="jean.dupont@example.com")
            salaire = st.number_input("💰 Salaire annuel (€)", min_value=0, value=45000, step=1000)
        
        with col2:
            nom = st.text_input("👤 Nom *", placeholder="Ex: Dupont")
            telephone = st.text_input("📞 Téléphone", placeholder="01.23.45.67.89")
            disponibilite = st.checkbox("✅ Disponible", value=True)
        
        notes = st.text_area("📝 Notes", height=100, placeholder="Notes sur le consultant...")
        
        # Bouton de soumission
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col2:
            submitted = st.form_submit_button("➕ Créer le consultant", 
                                            use_container_width=True,
                                            type="primary")
        
        if submitted:
            # Validation
            if not prenom or not nom or not email:
                st.error("❌ Veuillez remplir tous les champs obligatoires (*)")
            else:
                # Vérifier l'unicité de l'email
                existing_consultant = ConsultantService.get_consultant_by_email(email)
                if existing_consultant:
                    st.error(f"❌ Un consultant avec l'email {email} existe déjà !")
                else:
                    try:
                        # Données du nouveau consultant
                        consultant_data = {
                            'prenom': prenom.strip(),
                            'nom': nom.strip(),
                            'email': email.strip().lower(),
                            'telephone': telephone.strip() if telephone else None,
                            'salaire_actuel': salaire,
                            'disponibilite': disponibilite,
                            'notes': notes.strip() if notes else None
                        }
                        
                        # Créer le consultant
                        nouveau_consultant = ConsultantService.create_consultant(consultant_data)
                        
                        st.success(f"✅ {prenom} {nom} a été créé avec succès !")
                        st.info(f"🆔 ID: {nouveau_consultant.id}")
                        
                        # Rediriger vers le profil du nouveau consultant
                        if st.button("👁️ Voir le profil"):
                            st.session_state.view_consultant_profile = nouveau_consultant.id
                            st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la création: {e}")
